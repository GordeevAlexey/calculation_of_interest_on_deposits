PATH = f"""bd/DB.db"""

SQL_QUERY_GET_CONTRIBUTION_NAME = f"select distinct(name) from contribution "

SQL_QUERY_GET_CONTRIBUTION_DAY = f"select distinct(day) from contribution where name = ? "

SQL_QUERY_GET_CONTRIBUTION_SCHEMA = f"select distinct(chema_charges) from contribution " \
                                    f"where name = ? and day = ?"

SQL_QUERY_GET_CONTRIBUTION_PERCENT = f"select percent, extra_options, min_summa from contribution where " \
                                     f"name = ? and day = ? and chema_charges = ?"

SQL_QUERY_GET_CONTRIBUTION_EXTRA_OPTION = f"select options, percent from extra_options where " \
                                          f"contribution = ?"

SQL_QUERY_GET_CONTRIBUTION_EXTRA_OPTION_TXT = f"select distinct(text_message) from extra_options where " \
                                          f"contribution = ?"

SQL_QUERY_GET_CONTRIBUTION_WHERE_PERCENT = f"select distinct(where_percent) from contribution_where_percent where " \
                                          f"contribution = ?"

SQL_QUERY_GET_MAX_SUM = f"select max_summa from max_summa"
