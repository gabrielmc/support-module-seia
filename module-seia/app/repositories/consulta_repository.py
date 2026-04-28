import json
import logging, requests
from typing import List, Optional
from datetime import datetime
from app.core.config import settings
from requests.auth import HTTPDigestAuth
from app.core.database.conn_base import get_db_connection

logger = logging.getLogger("consulta_repository")

class ConsultaRepository:

    desenvolvimento = "DSV"
    homologacao = "HML"
    treinamento = "TRT"

    def buscar_datas_boletos(self, numeros_boletos: List[str]) -> dict:
        connection = None
        cursor = None
        try:
            sql = """
                SELECT
                    bpr.num_boleto,
                    bpr.dtc_pagamento,
                    bpr.dtc_vencimento
                FROM boleto_pagamento_requerimento bpr
                WHERE bpr.num_boleto = ANY(%s);
            """
            resultado = {}
            with get_db_connection(self.desenvolvimento) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (numeros_boletos,))
                    for num_boleto, dtc_pagamento, dtc_vencimento in cursor.fetchall():
                        resultado[num_boleto] = {
                            "dtc_pagamento": (
                                dtc_pagamento.strftime("%d/%m/%Y")
                                if dtc_pagamento else None
                            ),
                            "dtc_vencimento": (
                                dtc_vencimento.strftime("%d/%m/%Y")
                                if dtc_vencimento else None
                            )
                        }
            return resultado
        except Exception as e:
            logger.error(f"Erro em buscar_datas_boletos: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def buscar_boletos(self, numero_boleto: Optional[str],datas_pagamento: Optional[List[str]]):
        filtros = []
        params = {}
        connection = None
        cursor = None
        try:
            if numero_boleto:
                filtros.append("bpr.num_boleto = %(numero_boleto)s")
                params["numero_boleto"] = numero_boleto
            if datas_pagamento:
                filtros.append("bpr.dtc_pagamento::date = ANY(%(datas_pagamento)s)")
                params["datas_pagamento"] = datas_pagamento

            where_clause = " AND ".join(filtros) if filtros else "1=1"

            sql = f"""
                SELECT
                    bpr.num_boleto,
                    bpr.dtc_pagamento,
                    bpr.dtc_vencimento
                FROM boleto_pagamento_requerimento bpr
                WHERE {where_clause};
            """
            with get_db_connection(self.desenvolvimento) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro em buscar_boletos: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def monitorar_memoria_jboss(self, url: str):
        payload = {
            "operation": "read-resource",
            "address": [
                {"core-service": "platform-mbean"},
                {"type": "memory"}
            ],
            "include-runtime": "true"
        }
        try:
            user, password = self.definir_jboss_ambientes(url)
            response = requests.post(
                url,
                json=payload,
                auth=HTTPDigestAuth(user, password),
                timeout=10
            )
            if response.status_code != 200:
                raise Exception(f"Erro HTTP {response.status_code}")

            data = response.json()
            if data.get("outcome") != "success":
                raise Exception("JBoss retornou erro")

            non_heap = data["result"]["non-heap-memory-usage"]
            used_mb = round(non_heap["used"] / 1024 / 1024, 2)
            max_mb = round(non_heap.get("max", 0) / 1024 / 1024 or 256, 2)
            percentual = round((used_mb / max_mb) * 100, 2)
            return {
                "Usado_MB": used_mb,
                "Max_MB": max_mb,
                "Percentual": percentual
            }
        except Exception as e:
            logger.error(
                f"Erro ao consultar memória JBoss {url}: {str(e)}",
                exc_info=True
            )
            return {"erro": str(e)}

    def definir_jboss_ambientes(self, url: str):
        # Determinar credenciais baseado no ambiente de treinamento
        # TODO melhorar lógica para identificar ambiente, talvez usando regex ou configuração específica
        if "teste.sistema" in url:
            user = settings.JBOSS_USER_TREINAMENTO
            password = settings.JBOSS_PASS_TREINAMENTO
        else:
            user = settings.JBOSS_USER
            password = settings.JBOSS_PASS

        return user, password

    def monitorar_atualizacao_banco_old(self):
        try:
            sql = """
                SELECT
                    ct.dtc_tramitacao::date AS Data_Ultima_Tramitacao,
                    r.dtc_criacao::date AS Data_Ultimo_Requeirmento,
                    CASE
                        WHEN ct.dtc_tramitacao::date = r.dtc_criacao::date
                        THEN 'DATAS IGUAIS'
                        ELSE 'DATAS DIFERENTES'
                    END AS comparacao
                FROM
                    (SELECT dtc_tramitacao
                    FROM controle_tramitacao
                    ORDER BY dtc_tramitacao DESC
                    LIMIT 1) ct,
                    (SELECT dtc_criacao
                    FROM requerimento
                    ORDER BY dtc_criacao DESC
                    LIMIT 1) r;
            """
            ambientes = ["DSV", "HML", "TRT"]
            resultados = []
            for ambiente_nome in ambientes:
                print(f"Consultando ambiente: {ambiente_nome}")
                with get_db_connection(ambiente_nome) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)
                        resultado = cursor.fetchone()
                        if not resultado:
                            continue
                        data_tramitacao = resultado[0]
                        data_formatada = (
                            data_tramitacao.strftime("%d/%m/%Y")
                            if data_tramitacao else None
                        )
                        dias_desatualizado = (
                            (datetime.now().date() - data_tramitacao).days
                            if data_tramitacao else None
                        )
                        resultados.append({
                            "ambiente": ambiente_nome,
                            "data_ultima_tramitacao": data_formatada,
                            "dias_desatualizado": dias_desatualizado
                        })

            '''
            # Tenta obter do cache Redis
            cache_key = f"user_15874_carol.santana_seia"
            #comandos para teste de cache do REDIS (similar ao CRUD do RedisInsight)
            import redis
            redis_client = redis.Redis(host='localhost', port=6379, password='987321gabriel', db=0, decode_responses=True)
            redis_client.ping()
            print("✅ Conectado ao Redis com sucesso!")
            conteudo_armazenado = json.dumps(resultados, default=str)
            redis_client.set(cache_key, conteudo_armazenado, ex=3000)  # Armazena por 1 hora
            print(f"Dados salvos no Redis com sucesso! Tamanho: {len(conteudo_armazenado)} bytes")
            dados_recuperados_json = redis_client.get(cache_key)
            print(dados_recuperados_json)
            if dados_recuperados_json:
                # Converter JSON string de volta para objeto Python
                dados_armazenados = json.loads(dados_recuperados_json)
                print(f"📖 Dados recuperados do Redis: {dados_armazenados}")
                print(f"✅ Teste Redis concluído com sucesso!")
            else:
                print("❌ Falha ao recuperar dados do Redis")
            '''
            return resultados
        except Exception as e:
            logger.error(
                f"Erro em monitorar_atualizacao_banco: {str(e)}",
                exc_info=True
            )
            return None

    def monitorar_atualizacao_banco(self):
        sql = """
            SELECT
                ct.dtc_tramitacao::date AS Data_Ultima_Tramitacao,
                r.dtc_criacao::date AS Data_Ultimo_Requerimento,
                CASE
                    WHEN ct.dtc_tramitacao::date = r.dtc_criacao::date
                    THEN 'DATAS IGUAIS'
                    ELSE 'DATAS DIFERENTES'
                END AS comparacao
            FROM
                (SELECT dtc_tramitacao
                FROM controle_tramitacao
                ORDER BY dtc_tramitacao DESC
                LIMIT 1) ct,
                (SELECT dtc_criacao
                FROM requerimento
                ORDER BY dtc_criacao DESC
                LIMIT 1) r;
        """
        ambientes = ["DSV", "HML", "TRT"]
        resultados = []
        for ambiente_nome in ambientes:
            try:
                # Tenta obter conexão
                with get_db_connection(ambiente_nome) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)
                        resultado = cursor.fetchone()
                        if not resultado:
                            logger.warning(f"Nenhum resultado encontrado no ambiente {ambiente_nome}")
                            continue

                        data_tramitacao = resultado[0]
                        data_requerimento = resultado[1]
                        comparacao = resultado[2] if len(resultado) > 2 else None
                        # Formata as datas
                        data_formatada = (
                            data_tramitacao.strftime("%d/%m/%Y")
                            if data_tramitacao else None
                        )
                        dias_desatualizado = (
                            (datetime.now().date() - data_tramitacao).days
                            if data_tramitacao else None
                        )
                        #resultados.append({
                        #    "ambiente": ambiente_nome,
                        #    "data_ultima_tramitacao": data_formatada,
                        #    "data_ultimo_requerimento": data_requerimento.strftime("%d/%m/%Y") if data_requerimento else None,
                        #    "comparacao": comparacao,
                        #    "dias_desatualizado": dias_desatualizado,
                        #    "status": "ok"
                        #})
                        resultados.append({
                            "ambiente": ambiente_nome,
                            "data_ultima_tramitacao": data_formatada,
                            "dias_desatualizado": dias_desatualizado
                        })
            except Exception as e:
                logger.error(f"❌ Erro no ambiente {ambiente_nome}: {str(e)}", exc_info=True)
                # Adiciona resultado de erro para este ambiente
                resultados.append({
                    "ambiente": ambiente_nome,
                    "data_ultima_tramitacao": None,
                    "dias_desatualizado": None,
                    "status": "erro",
                    "erro": str(e)
                })
        return resultados
