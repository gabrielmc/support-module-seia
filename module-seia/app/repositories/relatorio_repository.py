import logging
from datetime import datetime
from app.core.database import get_db_connection

logger = logging.getLogger("relatorios_repository")

class RelatoriosRepository:
    
    desenvolvimento = "DSV"
    homologacao = "HML"

    def busca_zoneamento_uc(self, periodo: str) -> dict:
        connection = None
        cursor = None
        try:
            sql = """
                    SELECT p.num_processo AS processo,
                            CASE
                                    WHEN pes.ide_pessoa = pf.ide_pessoa_fisica THEN pf.nom_pessoa
                                    ELSE pj.nom_razao_social
                            END AS requerente,
                            CASE
                                    WHEN pes.ide_pessoa = pf.ide_pessoa_fisica THEN pf.num_cpf
                                    ELSE pj.num_cnpj
                            END AS cpf_cnpj,
                            e.nom_empreendimento AS nome_empreendimento,
                            t.des_tipologia AS tipologia_empreendimento,        
                            m.nom_municipio AS municipio_empreendimento,
                            CASE
                                    WHEN count(pa.ide_processo_ato) >= 2 THEN array_to_string(array_agg(DISTINCT aa.nom_ato_ambiental), '; ')
                                    ELSE max(DISTINCT aa.nom_ato_ambiental)
                            END AS "ato(s)",        
                            TO_CHAR(ct.dtc_tramitacao, 'dd/mm/yyyy') AS data_conclusao,
                            tspa.nom_tipo_status_processo_ato AS status_ato,
                            spa.num_prazo_validade AS validade_ato,
                                    CASE WHEN aa.ide_tipo_ato=1 THEN 
                                            st_transform(dg.the_geom,4674) 
                                    ELSE 
                                            st_transform(dg2.the_geom,4674)
                                    END  AS coordenadas
                    FROM
                            processo p
                    INNER JOIN controle_tramitacao ct ON
                            (p.ide_processo = ct.ide_processo)
                    INNER JOIN processo_ato pa ON
                            (p.ide_processo = pa.ide_processo)
                    LEFT JOIN status_processo_ato spa ON
                            (pa.ide_processo_ato = spa.ide_processo_ato
                                    AND spa.ide_status_processo_ato = (
                                    SELECT
                                            max(ide_status_processo_ato)
                                    FROM
                                            status_processo_ato spa2
                                    WHERE
                                            spa2.ide_processo_ato = pa.ide_processo_ato))
                    LEFT JOIN tipo_status_processo_ato tspa ON
                                    tspa.ide_tipo_status_processo_ato =spa.ide_tipo_status_processo_ato             
                    INNER JOIN ato_ambiental aa ON
                            (pa.ide_ato_ambiental = aa.ide_ato_ambiental)
                    INNER JOIN requerimento r ON
                            (p.ide_requerimento = r.ide_requerimento)
                    INNER JOIN requerimento_pessoa rp ON
                            (r.ide_requerimento = rp.ide_requerimento)
                    INNER JOIN pessoa pes ON
                            (rp.ide_pessoa = pes.ide_pessoa)
                    LEFT JOIN pessoa_fisica pf ON
                            (pes.ide_pessoa = pf.ide_pessoa_fisica)
                    LEFT JOIN pessoa_juridica pj ON
                            (pes.ide_pessoa = pj.ide_pessoa_juridica)
                    INNER JOIN empreendimento_requerimento er ON
                            (r.ide_requerimento = er.ide_requerimento)
                    INNER JOIN empreendimento e ON
                            (er.ide_empreendimento = e.ide_empreendimento)
                    INNER JOIN endereco_empreendimento ee ON
                            (e.ide_empreendimento = ee.ide_empreendimento)
                    INNER JOIN endereco e2 ON
                            (ee.ide_endereco = e2.ide_endereco)
                    INNER JOIN logradouro l ON
                            (e2.ide_logradouro = l.ide_logradouro)
                    INNER JOIN municipio m ON
                            (l.ide_municipio = m.ide_municipio)
                    INNER JOIN localizacao_geografica lg ON
                            (e.ide_localizacao_geografica = lg.ide_localizacao_geografica)
                    INNER JOIN dado_geografico dg ON
                            (lg.ide_localizacao_geografica = dg.ide_localizacao_geografica)
                    LEFT JOIN outorga o ON
                            (r.ide_requerimento = o.ide_requerimento)        
                    LEFT JOIN outorga_localizacao_geografica olg ON 
                            (o.ide_outorga = olg.ide_outorga)
                    LEFT JOIN outorga_concedida oc ON 
                            (olg.ide_outorga_localizacao_geografica = oc.ide_outorga_localizacao_geografica)
                    LEFT JOIN fce_outorga_localizacao_geografica folg ON
                            (oc.ide_fce_outorga_localizacao_geografica = folg.ide_fce_outorga_localizacao_geografica)
                    LEFT JOIN dado_geografico dg2 ON
                            (folg.ide_localizacao_geografica = dg2.ide_localizacao_geografica)     
                    INNER JOIN empreendimento_tipologia et ON
                            (e.ide_empreendimento = et.ide_empreendimento)
                    INNER JOIN tipologia_grupo tg ON
                            (et.ide_tipologia_grupo = tg.ide_tipologia_grupo)
                    INNER JOIN tipologia t ON
                            (tg.ide_tipologia = t.ide_tipologia)
                    WHERE
                            ct.dtc_tramitacao > %(periodo)s AND
                            ct.ide_status_fluxo = 2 
                            AND ct.ind_fim_da_fila = TRUE
                            AND pa.ind_excluido = FALSE
                            AND rp.ide_tipo_pessoa_requerimento = 1
                            AND aa.ide_tipo_ato IN (1,4)
                            AND spa.ide_tipo_status_processo_ato IN (5,7,8,9) 
                            AND ee.ide_tipo_endereco = 4
                    GROUP BY
                            processo,
                            data_conclusao,
                            requerente,
                            cpf_cnpj,
                            municipio_empreendimento,
                            tipologia_empreendimento,
                            nome_empreendimento,
                            coordenadas,
                            validade_ato,
                            status_ato
                    ORDER BY
                            processo DESC;
                    """
            periodo_dt = datetime.strptime( f"{periodo} 00:00", "%Y-%m-%d %H:%M")
            with get_db_connection(self.homologacao) as conn:
                with conn.cursor() as cursor:
                        cursor.execute(sql, {"periodo": periodo_dt})
                        colunas = [desc[0] for desc in cursor.description]
                        dados = cursor.fetchall()
            return {
                "colunas": colunas,
                "dados": dados
            }
        except Exception as e:
            logger.error(f"Erro em busca_zoneamento_uc: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
