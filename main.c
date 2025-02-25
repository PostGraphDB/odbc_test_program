//gcc main.c -L/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1 -I/opt/microsoft/msodbcsql18/include/ -g -o odbc_test -lodbc
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sql.h>
#include <sqlext.h>

#include <odbcinst.h>
#include <sqltypes.h>
#include <sqlucode.h>
#include <sqlspi.h>
//#include <msdasql.h>
//#include <msdadc.h>


void ReportStatus(RETCODE RetCode) {
    switch(RetCode)
    {
        case SQL_SUCCESS_WITH_INFO:
            fprintf(stderr, "Success With Info\n");
        case SQL_SUCCESS:
            fprintf(stderr, "Success\n");
            break;
        case SQL_ERROR:
            fprintf(stderr, "Error\n");
            break;
        case SQL_INVALID_HANDLE:
            fprintf(stderr, "Invalid Handle\n");
            break;
        case SQL_NO_DATA:
            fprintf(stderr, "No Data\n");
            break;
        case SQL_NEED_DATA:
            fprintf(stderr, "Need Data\n");
            break;
        case SQL_STILL_EXECUTING:
            fprintf(stderr,  "Still Executing\n");
            break;
        default:
            fprintf(stderr, "Unexpected return code %hd!\n", RetCode);
    }

}

int main(int argc, char **argv) {
    SQLHENV     hEnv = NULL;
    SQLHDBC     hDbc = NULL;
    SQLHSTMT    hStmt = NULL;
    SQLCHAR*    pwszConnStr = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=10.177.3.78;DATABASE=vectordb;UID=sa;PWD=1_SQLPerf;LongAsMax=yes;Connect Timeout=30;TrustServerCertificate=Yes;LongAsMax=yes;";
    WCHAR       wszInput[1000];
    SQLCHAR connStr[] = "DSN=PostgreSQL_DSN;";  
    SQLLEN cchDisplay;
    SQLLEN ssType;
    SQLINTEGER value; SQLLEN cbFetched;
    
    // Allocate an environment
    if (SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &hEnv) == SQL_ERROR) {
        fprintf(stderr, "Unable to allocate an environment handle\n");
        exit(-1);
    }

    ReportStatus(SQLSetEnvAttr(hEnv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0));
    ReportStatus(SQLAllocHandle(SQL_HANDLE_DBC, hEnv, &hDbc));

    // SQL Server
    ReportStatus(SQLDriverConnect(hDbc, NULL, pwszConnStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_COMPLETE));

    // Postgres
    //ReportStatus(SQLDriverConnect(hDbc, NULL, connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_COMPLETE));
    
    ReportStatus(SQLAllocHandle(SQL_HANDLE_STMT, hDbc, &hStmt));

/************************************************
Non-Paramatized Prepared Query - Works as Expected
*******************************************************/
/*
    fprintf(stderr, "Prepare: ");
    ReportStatus(SQLPrepare(hStmt, "SELECT 1 as id", strlen("SELECT 1 as id"))); 

    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);                                       



    //fprintf(stderr, "Prepare: ");
    //ReportStatus(SQLPrepare(hStmt, "SELECT 1 as id", strlen("SELECT 1 as id"))); 

    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
    
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);                                       


    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
    
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);                                       
*/

/********************************************************
Parameterized Integer - SQL_RESET_PARAMS Issue
***********************************************************/    
/*
    fprintf(stderr, "Parameterized Integer SQL_RESET_PARAMS\n");
    fprintf(stderr, "Prepare: ");
    //SQL Server
    ReportStatus(SQLPrepare(hStmt, "declare @v int; SELECT ? as id", strlen("declare @vint; SELECT ? as id"))); 
    
    // Postgres
    //ReportStatus(SQLPrepare(hStmt, "SELECT ?::int as id", strlen("SELECT ?::int as id"))); 


    fprintf(stderr, "Bind: ");
    SQLINTEGER v_reset = 2; SQLLEN l;
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_reset, 4, &l ));

    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));
    
    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
    
    // Problem Here
    //SQLFreeStmt(hStmt, SQL_RESET_PARAMS);       
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    //fprintf(stderr, "Bind: ");
    //ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_reset, 4, &l ));


    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
 
    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);   
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    fprintf(stderr, "Bind: ");
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_reset, 4, &l ));


    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
*/

/********************************************************
Parameterized Integer - SQLBindParameteri Pointer Issue
**********************************************************/    
/*
    fprintf(stderr, "Parameterized Integer SQLBindParameter\n");
    fprintf(stderr, "Prepare: ");
    //SQL Server
    ReportStatus(SQLPrepare(hStmt, "declare @v int; SELECT ? as id", strlen("declare @vint; SELECT ? as id"))); 
    
    // Postgres
    //ReportStatus(SQLPrepare(hStmt, "SELECT ?::int as id", strlen("SELECT ?::int as id"))); 


    fprintf(stderr, "Bind: ");
    SQLINTEGER v_bind_1 = 2; SQLLEN l_bind;
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_bind_1, 4, &l_bind ));

    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));


    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
    
    //SQLFreeStmt(hStmt, SQL_RESET_PARAMS);       
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    fprintf(stderr, "Bind: "); 
    SQLINTEGER v_bind_2 = 2;
    //v = 3;
    // Use new variable
     ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_bind_2, 4, &l_bind));


    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
 

    //SQLFreeStmt(hStmt, SQL_RESET_PARAMS);       
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    fprintf(stderr, "Bind: "); 
    //v = 3;
    // Use new variable
     ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_INTEGER, SQL_DECIMAL, 4, 0, &v_bind_2, 4, &l_bind ));


    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "SQLGetData: ");
    ReportStatus(SQLGetData(hStmt, (SQLUSMALLINT)(1), SQL_C_LONG, &value, sizeof(value), &cbFetched));
    fprintf(stderr, "Value %i\n", value);
*/
/********************************************************
Parameterized Vector
**********************************************************/    

    fprintf(stderr, "Parameterized Vector Start\n");
    

    /*********************************************************
        1st Query Prepare the Statement
    **********************************************************/    
    fprintf(stderr, "Prepare: ");
    ReportStatus(SQLPrepare(hStmt, "declare @v VECTOR(3); SELECT ? as id", strlen("declare @v VECTOR(3); SELECT ? as id"))); 

    // Postgres
    //ReportStatus(SQLPrepare(hStmt, "SELECT ?::text as id", strlen("SELECT ?::text as id"))); 


    fprintf(stderr, "Bind: ");
    SQLLEN l = 1;
    l = SQL_DATA_AT_EXEC;///sstrlen((char *)vec_str);
    SQLCHAR *vec_str = "[1, 2, 3]\0";
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, vec_str, sizeof((char *)vec_str), &l ));


    SQLCHAR varchar_value[100000]; // Buffer to store the VARCHAR data.  Make it large enough!
    SQLLEN varchar_len_or_ind; // To store the length or indicator (e.g., SQL_NULL_DATA)

    fprintf(stderr, "BindCol: ");
    ReportStatus(SQLBindCol(hStmt, 1, SQL_C_CHAR, &varchar_value, 100000, &varchar_len_or_ind));
 
    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));
    SQLRETURN ret;
    void* pInfo;
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    ReportStatus(ret = SQLPutData(hStmt, vec_str, SQL_NTS));
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "varhcar: %s", varchar_value);
   
    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);       
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    /*************************************************************
        2nd Query Do Not Reprepare the statement
    **************************************************************/
    SQLCHAR *vec_str2 = "[4, 5, 6]\0";
    SQLLEN l2 = 1;
    l2 = SQL_DATA_AT_EXEC;///sstrlen((char *)vec_str);
    
    fprintf(stderr, "Bind: ");
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, vec_str2, sizeof((char *) vec_str2), &l2 ));

    fprintf(stderr, "BindCol: ");
    ReportStatus(SQLBindCol(hStmt, 1, SQL_C_CHAR, &varchar_value, 100000, &varchar_len_or_ind));
 
    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    ReportStatus(ret = SQLPutData(hStmt, vec_str2, SQL_NTS));
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
 

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "varhcar: %s", varchar_value);
 
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    /****************************************************************
        3rd Query Memcpy to the existing buffers
    *****************************************************************/
    //SQLCHAR *
    vec_str2 = "[7, 8, 9]\0";
    //memcpy(vec_str2, vec_str3, sizeof(vec_str2));
    
    fprintf(stderr, "Execute: ");
    ReportStatus(SQLExecute(hStmt));

    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    ReportStatus(ret = SQLPutData(hStmt, vec_str, SQL_NTS));
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
 

    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));

    fprintf(stderr, "varhcar: %s", varchar_value);
 
/*************************************** Parameterized Vector ****************************************/    
/*
    fprintf(stderr, "Big Parameterized Vector Start\n");
    
    fprintf(stderr, "Prepare: ");
    // mssql
    ReportStatus(SQLPrepare(hStmt, "declare @v VARCHAR(MAX); SELECT ? as id", strlen("declare @v VARCHAR(MAX); SELECT ? as id"))); 

    // Postgres
    //ReportStatus(SQLPrepare(hStmt, "SELECT ?::text as id", strlen("SELECT ?::text as id"))); 

    fprintf(stderr, "Bind: ");
    SQLLEN l;
    SQLCHAR *vec_str = "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh\0";
    l = SQL_DATA_AT_EXEC;///sstrlen((char *)vec_str);
    fprintf(stderr, "l: %i\n", (int)l);
 
    fprintf(stderr, "Bind: ");
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_LONGVARCHAR, 0, 0, vec_str, 0, &l));
    //ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_LONGVARCHAR, 0, 0, vec_str, 0, &l ));

    SQLCHAR varchar_value[100000]; // Buffer to store the VARCHAR data.  Make it large enough!
    SQLLEN varchar_len_or_ind; // To store the length or indicator (e.g., SQL_NULL_DATA)

    fprintf(stderr, "BindCol: ");
    ReportStatus(SQLBindCol(hStmt, 1, SQL_C_CHAR, &varchar_value, 100000, &varchar_len_or_ind));
 
    fprintf(stderr, "Execute: ");
    RETCODE ret;
    ReportStatus(ret = SQLExecute(hStmt));

    void* pInfo;
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    ReportStatus(ret = SQLPutData(hStmt, vec_str, SQL_NTS));
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    
    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));
    fprintf(stderr, "Result: %s\n", varchar_value);
    fprintf(stderr, "l: %i\n", (int)l);

    SQLLEN cRows = -1;
    ret = SQLRowCount(hStmt, &cRows);
    fprintf(stderr, "cRows: %i\n", (int)cRows);

    SQLSMALLINT cCols = 0;
    ret = SQLNumResultCols(hStmt, &cCols);
    fprintf(stderr, "cCols: %i\n", (int)cCols);

    SQLFreeStmt(hStmt, SQL_RESET_PARAMS);                                       
    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);

    SQLCHAR *vec_str_2 = "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj\0";
    l = SQL_DATA_AT_EXEC;///strlen((char *)vec_str);
    fprintf(stderr, "l: %i\n", (int)l);
    
    fprintf(stderr, "Bind: ");
    ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_LONGVARCHAR, 0, 0, vec_str, 0, &l ));
 
    fprintf(stderr, "Execute: ");
    ReportStatus(ret = SQLExecute(hStmt));

    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    ReportStatus(ret = SQLPutData(hStmt, vec_str_2, SQL_NTS));
    ReportStatus(ret = SQLParamData(hStmt, (SQLPOINTER*)pInfo));
    
    fprintf(stderr, "Fetch: ");
    ReportStatus(SQLFetch(hStmt));
    fprintf(stderr, "Result: %s\n", varchar_value);
    fprintf(stderr, "l: %i\n", (int)l);

    SQLFreeStmt(hStmt, SQL_UNBIND);                                       
    SQLFreeStmt(hStmt, SQL_CLOSE);
*/
/*********************************** End ***************************************/
    
    SQLDisconnect(hEnv);

}
