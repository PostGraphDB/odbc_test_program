
This repo contains 4 query examples to highlight some behavior of the ODBC driver for SQL Server. To use, we recommend turning on the SQL Server Profiler to view the issue. 

The point is to highlight a potential issue with Prepared Statements. 

This repo simpiifies an issue that our team found in the code for pyODBC that is used by VectorDBBench. The first query simplifies what is happening for every call to the execute method from python using pyODBC. The next query shows a small change where we take out the call to SQLPrepare and we expect the Prepared Statement from the previous query to be reused. The following two queries are examples of ways to get the Prepared Statement to be reused with some alterations to the first and second queries.

The key point to highlight with these queries is the setting of the parameter length to SQL_DATA_AT_EXEC. Which tells the Microsoft ODBC driver that the parameter will be sent to the server after SQLExecute is called. While this is not necessary for the parameters provided in these examples, when discussing parameteters of any significant size (vectors of at least 768 dimensions) this becomes an absolute necessity and will be used by pyODBC. 

```C
SQLLEN l = SQL_DATA_AT_EXEC;
```

## Example Query 1
This query prepares the query to run and then runs the query. In the Profiler, we receive a "PREPARE SQL" log line from this query. The results are returned as expected. This is query is meant to be a very simplified version of the behavior run in pyODBC.

One of the key lines in this code is the call to SQLBindParameter. This method call is called for every call to execute in pyODBC. See the sub-section below for how Postgres behaves in this circumstance, as this is the difference in functionality between Postgres and SQL Server that we are trying to highlight.  

```C
ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, vec_str, sizeof((char *)vec_str), &l ));
```

The improtant lines that will be key to the next query are the clean up routines:

```C
SQLFreeStmt(hStmt, SQL_RESET_PARAMS);       
SQLFreeStmt(hStmt, SQL_UNBIND);                                       
SQLFreeStmt(hStmt, SQL_CLOSE);
```


### Postgres Behavior

If you were to run this query in Postgres then what would happen is this query would have between 6 and 7 network calls. 1 call to prepare the query, 2 calls to a synchronization routine, 1 call to describe the output columns from this query, 1 call to bind the parameters, 1 call to execute the query and maybe one call to a direct execution of a transaction maintainance routine query.

If one were to copy paste the all the code for this query, excluding just the SQLPrepare command, there would be only three network calls in future calls (describe, bind and execute).


## Example Query 2
This query, does not call SQLPrepare, yet when running the query, SQL Profiler will log an UNPREPARE command and then it will call PREPARE again. This query is representative of what we are seeing in pyODBC.

SQLBindParameter must be called again, because we called SQLFreeStmt function with the SQL_RESET_PARAMS parameter in the cleanup of the previous query

```C
ReportStatus(SQLBindParameter(hStmt, (SQLUSMALLINT)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, &vec_str2, sizeof(vec_str2), &l2 ));
```

For the next query we will take out the call to SQLFreeStmt function with the SQL_RESET_PARAMS parameter

```C
SQLFreeStmt(hStmt, SQL_UNBIND);                                       
SQLFreeStmt(hStmt, SQL_CLOSE);
```

## Example Query 3
This query will call the Prepared Statement without the reprepare that is listed above. 

This query will copy the new parameter data into the existing memory block allocated for the parameter.

```C
    SQLCHAR vec_str3[10] = "[7, 8, 9]\0";
    memcpy(&vec_str2, &vec_str3, sizeof(vec_str2));
```

This query demonstrates the expected behavior that we desire in pyODBC (the reuse of Prepared Statements).

For the next query we will take out the call to  SQLFreeStmt function with the SQL_UNBIND parameter

```C
    SQLFreeStmt(hStmt, SQL_CLOSE);
```

## Example Query 4
This query simplifies the process even futher.

We are able to send the parameter data without use of the allocated buffer for the parameter data at all, we can just send the data via the SQLPutData call

```C
ReportStatus(ret = SQLPutData(hStmt, &vec_str4, SQL_NTS));
```


## Build Command
gcc main.c -L/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1 -I/opt/microsoft/msodbcsql18/include/ -g -o odbc_test -lodbc
