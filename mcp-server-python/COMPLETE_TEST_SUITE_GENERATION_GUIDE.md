# Complete Test Suite Generation Guide
## From MCP Server Connection to Full Test Suite Creation

**Date:** October 21, 2025  
**Author:** Generated Documentation  
**Database:** AHS-LP-945 / Ahs_Bit_Red_QA_8170  
**Environment:** VS Code with MCP Integration

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: MCP Server Setup](#step-1-mcp-server-setup)
4. [Step 2: Connect to MCP Server](#step-2-connect-to-mcp-server)
5. [Step 3: Analyze Stored Procedure](#step-3-analyze-stored-procedure)
6. [Step 4: Generate Test Cases](#step-4-generate-test-cases)
7. [Step 5: Create INIT Procedure](#step-5-create-init-procedure)
8. [Step 6: Create DTD Procedure](#step-6-create-dtd-procedure)
9. [Step 7: Create UT Procedure](#step-7-create-ut-procedure)
10. [Step 8: Execute and Validate](#step-8-execute-and-validate)
11. [Examples of Complete Test Suites](#examples-of-complete-test-suites)
12. [Troubleshooting](#troubleshooting)
13. [Best Practices](#best-practices)

---

## Overview

This guide documents the complete workflow for generating comprehensive test suites for SQL Server stored procedures using:
- **MCP (Model Context Protocol)** for database connectivity
- **VS Code Copilot** for intelligent test generation
- **UT (Unit Testing) Framework** for test management

### What You'll Create

For each stored procedure, you'll generate:
1. ✅ Test Cases File - Manual test execution scripts
2. ✅ INIT Procedure - Test framework initialization
3. ✅ DTD Procedure - Dynamic test data preparation
4. ✅ UT Procedure - Automated test execution
5. ✅ README Documentation - Usage guide

---

## Prerequisites

### Required Software
- ✅ Visual Studio Code
- ✅ Python 3.13 or later
- ✅ SQL Server Management Studio (SSMS) - optional but recommended
- ✅ ODBC Driver 17 for SQL Server

### Required Python Packages
```bash
pip install pyodbc
pip install mcp
pip install python-dotenv
pip install aiohttp
```

### Database Requirements
- ✅ Access to SQL Server instance
- ✅ Appropriate database permissions
- ✅ UT schema with required tables:
  - `UT.OBJECT_DETAILS`
  - `UT.OBJECT_PARAM`
  - `UT.TEST_RUNS_CONFIG`
  - `UT.TEST_PARAM_DATA`
  - `UT.TEST_RUNS_LOG`
  - `UT.Resource_details`

### VS Code Setup
- ✅ MCP extension configured
- ✅ GitHub Copilot enabled
- ✅ Python extension installed

---

## Step 1: MCP Server Setup

### 1.1 Create MCP Configuration

Create or verify `.vscode/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "python",
      "args": [
        "-u",
        "C:\\Users\\ajay.singh\\Downloads\\test\\mcp-server-python\\server.py"
      ],
      "env": {
        "DB_SERVER": "AHS-LP-945",
        "DB_NAME": "Ahs_Bit_Red_QA_8170",
        "DB_USER": "",
        "DB_PASSWORD": "",
        "PYTHONPATH": "C:\\Users\\ajay.singh\\Downloads\\test\\mcp-server-python",
        "PATH": "C:\\Users\\ajay.singh\\Downloads\\test\\.venv\\Scripts;${env:PATH}"
      }
    }
  }
}
```

**Key Configuration Points:**
- `command`: Path to Python executable (uses system Python or venv)
- `args`: Path to your `server.py` file
- `env`: Database connection details
- Empty `DB_USER` and `DB_PASSWORD` = Windows Authentication

### 1.2 Verify Python Environment

```powershell
# Activate virtual environment (if using venv)
.\.venv\Scripts\Activate.ps1

# Verify Python version
python --version

# Verify required packages
pip list | findstr "pyodbc mcp aiohttp"
```

### 1.3 Test MCP Server (Optional)

The MCP server automatically starts when you use Copilot Chat in VS Code. You can verify it's working by:

1. Open VS Code Copilot Chat
2. Ask: "connect to the mcp server"
3. Verify connection success

---

## Step 2: Connect to MCP Server

### 2.1 Connect via Copilot Chat

In VS Code Copilot Chat, type:
```
connect to the mcp server
```

### 2.2 Verify Connection

Use MCP tools to verify connectivity:

**List all tables:**
```
@workspace Can you list all tables in the database?
```

**List stored procedures:**
```
@workspace Can you list stored procedures with pattern 'USP_AHS%'?
```

### 2.3 MCP Tools Available

Once connected, you have access to:

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `connect_database` | Connect to SQL Server | Auto-connects via config |
| `list_tables` | List all tables | Get table names |
| `describe_table` | Get table structure | Analyze table columns |
| `list_stored_procedures` | List procedures | Find procedures by pattern |
| `get_procedure_details` | Get procedure info | Retrieve parameters & definition |
| `execute_query` | Run SQL queries | Query test data |
| `execute_stored_procedure` | Execute procedure | Test procedure execution |
| `get_related_tables` | Get FK relationships | Understand data model |

---

## Step 3: Analyze Stored Procedure

### 3.1 Request Procedure Analysis

In Copilot Chat:
```
Review the SQL Server stored procedure named USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
and provide me with:
1. List of all parameters with data types
2. Purpose of the procedure
3. Return columns (if determinable)
```

### 3.2 What Copilot Returns

Copilot will analyze and provide:

**Parameter List:**
```sql
@HEALTH_COACH_ID BIGINT
@ALTRUISTA_ID NVARCHAR(100)
@RISK_CATEGORY_ID VARCHAR(100)
@FIRST_NAME VARCHAR(100)
@LAST_NAME VARCHAR(100)
@PAGE_NUMBER INT
@PAGE_SIZE INT
@ORDER_BY_FIELD VARCHAR(200)
@SORT_ORDER VARCHAR(4)
@IS_CURRENTLY_ENROLLED BIT
@MY_CARE_TEAM_SEARCH TINYINT
@LOGIN_USERID BIGINT
@CLIENT_TIME DATETIME
@CS_VIEW_SENSITIVE BIT
@FIELD_NAMES VARCHAR(8000)
@SHOW_ACTIVE_RECORDS TINYINT
@RISK_TYPE_ID INT
@LOB_BEN_ID_FILTER BIGINT
```

**Business Logic Summary:**
- Purpose: Retrieves filtered, paginated care member list
- Features: Pagination, sorting, filtering, search
- Security: Sensitive diagnosis view control

### 3.3 Document Findings

Create notes about:
- Required vs optional parameters
- Parameter dependencies
- Valid value ranges
- Business rules to test

---

## Step 4: Generate Test Cases

### 4.1 Request Test Case Generation

In Copilot Chat:
```
Review the SQL Server stored procedure named USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
and generate the following:

1. Test Cases: Provide at least 3 positive test cases and 3 negative test cases 
   covering various parameter combinations
2. Save the test cases to templates folder
```

### 4.2 Test Case Structure

Copilot generates test cases following this pattern:

```sql
-- =============================================
-- Test Cases for USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
-- Generated: October 21, 2025
-- =============================================

-- POSITIVE TEST CASES
-- =============================================

-- Test Case 1: Basic execution with required parameters
EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
    @HEALTH_COACH_ID = 15894099,
    @PAGE_NUMBER = 1,
    @PAGE_SIZE = 20,
    @ORDER_BY_FIELD = 'FIRST_NAME',
    @SORT_ORDER = 'ASC',
    @MY_CARE_TEAM_SEARCH = 1,
    @SHOW_ACTIVE_RECORDS = 0;

-- Test Case 2: With search filters
EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
    @HEALTH_COACH_ID = 15894099,
    @ALTRUISTA_ID = 'Alt_12345',
    @FIRST_NAME = 'John',
    @LAST_NAME = 'Smith',
    @PAGE_NUMBER = 1,
    @PAGE_SIZE = 20,
    @ORDER_BY_FIELD = 'FIRST_NAME',
    @SORT_ORDER = 'ASC',
    @MY_CARE_TEAM_SEARCH = 1,
    @SHOW_ACTIVE_RECORDS = 0;

-- NEGATIVE TEST CASES
-- =============================================

-- Test Case 17: Invalid HEALTH_COACH_ID
EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
    @HEALTH_COACH_ID = -99999,
    @PAGE_NUMBER = 1,
    @PAGE_SIZE = 20;

-- Test Case 18: Invalid PAGE_NUMBER (zero)
EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
    @HEALTH_COACH_ID = 15894099,
    @PAGE_NUMBER = 0,
    @PAGE_SIZE = 20;
```

### 4.3 Test Case Coverage

Ensure your test cases cover:

**Positive Scenarios:**
- ✅ Minimum required parameters
- ✅ All parameters with valid values
- ✅ Pagination variations
- ✅ Sorting options
- ✅ Filter combinations
- ✅ Search modes
- ✅ Edge cases (boundary values)

**Negative Scenarios:**
- ✅ NULL required parameters
- ✅ Invalid parameter values
- ✅ Out-of-range values
- ✅ Invalid data types (SQL injection attempts)
- ✅ Invalid combinations

### 4.4 Generated File

**File:** `templates/USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_TestCases.sql`

---

## Step 5: Create INIT Procedure

### 5.1 Request INIT Procedure Generation

In Copilot Chat:
```
Create the INIT procedure for USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
using the template TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_INIT.sql

Use:
- @BaseTestCaseID = 2900
- @ObjectID = 185
```

### 5.2 INIT Procedure Structure

The INIT procedure contains 4 main sections:

#### Section 1: Object Registration
```sql
-- Register the stored procedure in OBJECT_DETAILS
INSERT INTO UT.OBJECT_DETAILS 
(
    OBJECT_ID,
    OBJECT_NAME,
    OBJECT_PURPOSE_ID,
    OBJECT_TYPE_ID,
    OBJECT_DESCRIPTION,
    SCHEMA_NAME,
    IS_ACTIVE,
    CREATED_BY,
    CREATED_DATE
)
VALUES 
(
    185,  -- @ObjectID
    'USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT',
    1,    -- Purpose ID
    1,    -- Type: Stored Procedure
    'Retrieves filtered and paginated care member list',
    'dbo',
    1,    -- Active
    999,  -- System user
    GETDATE()
);
```

#### Section 2: Parameter Definitions
```sql
-- Define all 18 parameters
INSERT INTO UT.OBJECT_PARAM 
(
    OBJECT_ID,
    PARAM_SEQ_NO,
    PARAM_NAME,
    PARAM_DATATYPE,
    PARAM_LENGTH,
    IS_MANDATORY,
    DEFAULT_VALUE,
    PARAM_DESCRIPTION,
    CREATED_BY,
    CREATED_DATE
)
VALUES
(185, 1, 'HEALTH_COACH_ID', 'BIGINT', 8, 1, NULL, 'Care coach/staff member ID', 999, GETDATE()),
(185, 2, 'ALTRUISTA_ID', 'NVARCHAR', 100, 0, NULL, 'Client patient identifier', 999, GETDATE()),
(185, 3, 'RISK_CATEGORY_ID', 'VARCHAR', 100, 0, NULL, 'Comma-separated risk category IDs', 999, GETDATE()),
-- ... (15 more parameters)
```

#### Section 3: Test Case Configuration
```sql
-- Define 15 test cases
INSERT INTO UT.TEST_RUNS_CONFIG 
(
    TEST_CASE_ID,
    OBJECT_ID,
    TEST_CASE_OBJECT,
    TEST_CASE_NAME,
    TEST_CASE_DESCRIPTION,
    TEST_CASE_TYPE,
    IS_ACTIVE,
    CREATED_BY,
    CREATED_DATE
)
VALUES
(2001, 185, '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]', 
 'TC_2001_BasicExecution', 'Test basic execution with required parameters', 'POSITIVE', 1, 999, GETDATE()),
 
(2002, 185, '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]', 
 'TC_2002_WithSearchFilters', 'Test with ALTRUISTA_ID, FIRST_NAME, LAST_NAME filters', 'POSITIVE', 1, 999, GETDATE()),
-- ... (13 more test cases)
```

#### Section 4: Parameter Values
```sql
-- Insert parameter values for each test case
INSERT INTO UT.TEST_PARAM_DATA 
(
    TEST_CASE_ID,
    PARAM_SEQ_NO,
    PARAM_NAME,
    PARAM_VALUE,
    CREATED_BY,
    CREATED_DATE
)
VALUES
-- Test Case 2001: Basic Execution
(2001, 1, 'HEALTH_COACH_ID', '15894099', 999, GETDATE()),
(2001, 2, 'PAGE_NUMBER', '1', 999, GETDATE()),
(2001, 3, 'PAGE_SIZE', '20', 999, GETDATE()),
-- ... (more parameters)
```

### 5.3 Execute INIT Procedure

```sql
-- Run INIT to set up test framework
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_INIT]
    @BaseTestCaseID = 2900,
    @ObjectID = 185
```

### 5.4 Verify INIT Execution

```sql
-- Verify object registration
SELECT * FROM UT.OBJECT_DETAILS WHERE OBJECT_ID = 185;

-- Verify parameters
SELECT * FROM UT.OBJECT_PARAM WHERE OBJECT_ID = 185 ORDER BY PARAM_SEQ_NO;

-- Verify test cases
SELECT * FROM UT.TEST_RUNS_CONFIG 
WHERE TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
ORDER BY TEST_CASE_ID;

-- Verify parameter data
SELECT * FROM UT.TEST_PARAM_DATA 
WHERE TEST_CASE_ID BETWEEN 2001 AND 2025
ORDER BY TEST_CASE_ID, PARAM_SEQ_NO;
```

### 5.5 Generated File

**File:** `templates/TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_INIT.sql`

---

## Step 6: Create DTD Procedure

### 6.1 Request DTD Procedure Generation

In Copilot Chat:
```
Create the DTD (Dynamic Test Data) procedure for USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
using the template TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD.sql

Query the database to get valid values for:
- HEALTH_COACH_ID
- ALTRUISTA_ID
- RISK_CATEGORY_ID
- FIRST_NAME, LAST_NAME
- RISK_TYPE_ID
- LOB_BEN_ID_FILTER

Update TEST_PARAM_DATA with these values for positive test cases.
```

### 6.2 DTD Procedure Structure

The DTD procedure dynamically prepares test data:

#### Query Valid Data
```sql
-- Get Valid HEALTH_COACH_ID
DECLARE @ValidHealthCoachID BIGINT;

SET @sqlCommand = N'SELECT TOP 1 @HealthCoachID = CSD.MEMBER_ID
FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.CARE_STAFF_DETAILS CSD
    INNER JOIN ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.ROLE R
        ON CSD.ROLE_ID = R.ROLE_ID
WHERE CSD.STATUS_ID = 1
  AND EXISTS (
      SELECT 1 
      FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.MEMBER_CARESTAFF MC
      WHERE MC.MEMBER_ID = CSD.MEMBER_ID
        AND MC.IS_ACTIVE = 1
  )
ORDER BY NEWID()';

SET @paramDefinition = N'@HealthCoachID BIGINT OUTPUT';
EXEC sp_executesql @sqlCommand, @paramDefinition, 
    @HealthCoachID = @ValidHealthCoachID OUTPUT;

-- Fallback if no valid data found
IF @ValidHealthCoachID IS NULL
    SET @ValidHealthCoachID = 15894099;
```

#### Update Test Data
```sql
-- Update parameters for POSITIVE test cases
IF @TestCaseType = 'POSITIVE'
BEGIN
    -- Test Case 2001: Basic execution
    IF @TestCaseID = 2001
    BEGIN
        EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
            @TEST_CASE_ID = @TestCaseID, 
            @PARAM_NAME = 'HEALTH_COACH_ID', 
            @PARAM_VALUE = @ValidHealthCoachID;
    END

    -- Test Case 2002: With search filters
    IF @TestCaseID = 2002
    BEGIN
        EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
            @TEST_CASE_ID = @TestCaseID, 
            @PARAM_NAME = 'HEALTH_COACH_ID', 
            @PARAM_VALUE = @ValidHealthCoachID;
            
        EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
            @TEST_CASE_ID = @TestCaseID, 
            @PARAM_NAME = 'ALTRUISTA_ID', 
            @PARAM_VALUE = @ValidAltruistaID;
    END
    -- ... (more test cases)
END
```

### 6.3 DTD Best Practices

**Do:**
- ✅ Query actual database for valid test data
- ✅ Provide fallback values
- ✅ Use NEWID() for random selection
- ✅ Filter by active/valid records only
- ✅ Handle NULL cases gracefully

**Don't:**
- ❌ Hard-code all values
- ❌ Assume data exists
- ❌ Use invalid/deleted records
- ❌ Update NEGATIVE test cases with valid data

### 6.4 Execute DTD Procedure

```sql
-- Update all test cases
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @TEST_CASE_ID = NULL;

-- Update specific test case
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @TEST_CASE_ID = 2001;
```

### 6.5 Verify DTD Execution

```sql
-- Check updated parameter values
SELECT 
    TPD.TEST_CASE_ID,
    TRC.TEST_CASE_NAME,
    TPD.PARAM_NAME,
    TPD.PARAM_VALUE,
    TPD.MODIFIED_DATE
FROM UT.TEST_PARAM_DATA TPD
    INNER JOIN UT.TEST_RUNS_CONFIG TRC ON TPD.TEST_CASE_ID = TRC.TEST_CASE_ID
WHERE TRC.TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
    AND TPD.MODIFIED_DATE IS NOT NULL
ORDER BY TPD.TEST_CASE_ID, TPD.PARAM_SEQ_NO;
```

### 6.6 Generated File

**File:** `templates/TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD.sql`

---

## Step 7: Create UT Procedure

### 7.1 Request UT Procedure Generation

In Copilot Chat:
```
Create the UT (Unit Test) procedure for USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
using the template TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED_UT.sql

Include:
- Call to DTD procedure before test execution
- #Actual temp table for results
- Dynamic SQL execution via linked server
- Error handling
- Logging to TEST_RUNS_LOG
- Debug modes (0, 1, 2)
- Summary reporting
```

### 7.2 UT Procedure Structure

#### Section 1: Setup and DTD Call
```sql
CREATE OR ALTER PROCEDURE [UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]
    @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170', 
    @SERVER_NAME VARCHAR(30) = 'AHS-LP-945', 
    @TEST_CASE_ID INT = NULL, 
    @debug INT = 2
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Call DTD to prepare test data
    IF @TEST_CASE_ID IS NULL
        EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD] 
            @DEST_DB_NAME = @DEST_DB_NAME, @TEST_CASE_ID = NULL
    ELSE
        EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD] 
            @DEST_DB_NAME = @DEST_DB_NAME, @TEST_CASE_ID = @TEST_CASE_ID
```

#### Section 2: Temp Table Definition
```sql
    -- Define temp table to match procedure output
    CREATE TABLE #Actual (
        PATIENT_ID BIGINT,
        ALTRUISTA_ID VARCHAR(100),
        FIRST_NAME VARCHAR(100),
        LAST_NAME VARCHAR(100),
        PATIENT_NAME VARCHAR(255),
        PHONE_NUMBER VARCHAR(50),
        EMAIL_ADDRESS VARCHAR(255),
        DATE_OF_BIRTH DATE,
        AGE INT,
        GENDER VARCHAR(50),
        RISK_CATEGORY VARCHAR(100),
        RISK_CATEGORY_ID INT,
        RISK_SCORE DECIMAL(10,2),
        ENROLLMENT_STATUS VARCHAR(50),
        IS_CURRENTLY_ENROLLED BIT,
        PROGRAM_NAME VARCHAR(255),
        CARE_COACH_NAME VARCHAR(255),
        LAST_CONTACT_DATE DATETIME,
        NEXT_CONTACT_DATE DATETIME,
        TOTAL_RECORDS INT,
        ROW_NUMBER INT
    );
```

#### Section 3: Test Execution Loop
```sql
    -- Loop through test cases
    WHILE @Index <= @Total
    BEGIN
        -- Build dynamic SQL with parameters
        DECLARE TestParam_cursor CURSOR FOR
        SELECT [PARAM_NAME], [PARAM_VALUE]
        FROM [UT].[TEST_PARAM_DATA]
        WHERE TEST_CASE_ID = @TestCaseID
        ORDER BY PARAM_SEQ_NO;
        
        OPEN TestParam_cursor;
        FETCH NEXT FROM TestParam_cursor INTO @ParamName, @ParamValue;
        
        WHILE @@FETCH_STATUS = 0
        BEGIN
            IF @ParamValue IS NULL OR @ParamValue = 'NULL'
                SET @Param_Concat = @Param_Concat + '@' + @ParamName + ' = NULL, ';
            ELSE
                SET @Param_Concat = @Param_Concat + '@' + @ParamName + ' = ''' + @ParamValue + ''', ';
            
            FETCH NEXT FROM TestParam_cursor INTO @ParamName, @ParamValue;
        END
        
        CLOSE TestParam_cursor;
        DEALLOCATE TestParam_cursor;
```

#### Section 4: Execute and Log
```sql
        -- Execute via linked server
        SET @sqlCommand = 'INSERT INTO #Actual ' +
                         'SELECT * FROM OPENQUERY([' + @SERVER_NAME + '], ''SET NOCOUNT ON; ' +
                         'EXEC ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.' + @TestCaseName + ' ' + 
                         REPLACE(@Param_Concat, '''', '''''') + ''')';
        
        IF @debug = 2
        BEGIN
            BEGIN TRY
                EXEC sp_executesql @sqlCommand;
                SET @TestOutcome = 'PASS';
            END TRY
            BEGIN CATCH
                SET @TestOutcome = 'FAIL';
                SET @ErrorMessage = ERROR_MESSAGE();
            END CATCH
        END
        
        -- Log results
        INSERT INTO [UT].[TEST_RUNS_LOG]
        (RUN_ID, TEST_CASE_ID, START_TIME, END_TIME, TEST_OUTCOME, ERROR_MESSAGE, CREATED_BY, CREATED_DATE)
        VALUES
        (@RUN_ID, @TestCaseID, @START_TIME, @END_TIME, @TestOutcome, @ErrorMessage, @CreatedBy, GETDATE());
    END
```

#### Section 5: Summary Report
```sql
    -- Display summary
    SELECT 
        TEST_OUTCOME,
        COUNT(*) AS TEST_COUNT
    FROM [UT].[TEST_RUNS_LOG]
    WHERE RUN_ID = @RUN_ID
    GROUP BY TEST_OUTCOME;
    
    -- Display detailed results
    SELECT 
        TRL.TEST_CASE_ID,
        TRC.TEST_CASE_DESCRIPTION,
        TRL.TEST_OUTCOME,
        DATEDIFF(MILLISECOND, TRL.START_TIME, TRL.END_TIME) AS EXECUTION_TIME_MS,
        TRL.ERROR_MESSAGE
    FROM [UT].[TEST_RUNS_LOG] TRL
        INNER JOIN [UT].[TEST_RUNS_CONFIG] TRC ON TRL.TEST_CASE_ID = TRC.TEST_CASE_ID
    WHERE TRL.RUN_ID = @RUN_ID
    ORDER BY TRL.TEST_CASE_ID;
END;
```

### 7.3 Debug Modes

The UT procedure supports three debug modes:

| Mode | Behavior | Use Case |
|------|----------|----------|
| **0** | Silent - No output, only logs to database | Production/automated testing |
| **1** | Print SQL only - Show commands without executing | Review SQL before execution |
| **2** | Full execution - Run tests and show detailed output | Development/debugging |

### 7.4 Execute UT Procedure

```sql
-- Execute all tests with full debug
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @SERVER_NAME = 'AHS-LP-945',
    @TEST_CASE_ID = NULL,
    @debug = 2;

-- Execute specific test case
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @SERVER_NAME = 'AHS-LP-945',
    @TEST_CASE_ID = 2001,
    @debug = 2;

-- Print SQL only (no execution)
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @SERVER_NAME = 'AHS-LP-945',
    @TEST_CASE_ID = NULL,
    @debug = 1;
```

### 7.5 Generated File

**File:** `templates/TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_UT.sql`

---

## Step 8: Execute and Validate

### 8.1 Complete Execution Workflow

```sql
-- Step 1: Initialize test framework
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_INIT]
    @BaseTestCaseID = 2900,
    @ObjectID = 185;

-- Step 2: Prepare dynamic test data
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @TEST_CASE_ID = NULL;

-- Step 3: Execute tests
EXEC UT.[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]
    @DEST_DB_NAME = 'Ahs_Bit_Red_QA_8170',
    @SERVER_NAME = 'AHS-LP-945',
    @TEST_CASE_ID = NULL,
    @debug = 2;
```

### 8.2 Analyze Test Results

#### View Summary
```sql
-- Get latest test run summary
SELECT 
    RUN_ID,
    TEST_OUTCOME,
    COUNT(*) AS TEST_COUNT,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS PERCENTAGE
FROM UT.TEST_RUNS_LOG
WHERE RUN_ID = (
    SELECT MAX(RUN_ID) 
    FROM UT.TEST_RUNS_LOG 
    WHERE TEST_CASE_ID IN (
        SELECT TEST_CASE_ID 
        FROM UT.TEST_RUNS_CONFIG 
        WHERE TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
    )
)
GROUP BY RUN_ID, TEST_OUTCOME
ORDER BY TEST_OUTCOME;
```

#### View Detailed Results
```sql
-- Get detailed test results
SELECT 
    TRL.TEST_CASE_ID,
    TRC.TEST_CASE_NAME,
    TRC.TEST_CASE_DESCRIPTION,
    TRC.TEST_CASE_TYPE,
    TRL.TEST_OUTCOME,
    DATEDIFF(MILLISECOND, TRL.START_TIME, TRL.END_TIME) AS EXECUTION_TIME_MS,
    TRL.ERROR_MESSAGE,
    TRL.CREATED_DATE
FROM UT.TEST_RUNS_LOG TRL
    INNER JOIN UT.TEST_RUNS_CONFIG TRC ON TRL.TEST_CASE_ID = TRC.TEST_CASE_ID
WHERE TRC.TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
    AND TRL.RUN_ID = (
        SELECT MAX(RUN_ID) 
        FROM UT.TEST_RUNS_LOG 
        WHERE TEST_CASE_ID = TRL.TEST_CASE_ID
    )
ORDER BY TRL.TEST_CASE_ID;
```

#### View Failed Tests Only
```sql
-- Get only failed tests
SELECT 
    TRL.TEST_CASE_ID,
    TRC.TEST_CASE_DESCRIPTION,
    TRL.ERROR_MESSAGE,
    TRL.CREATED_DATE
FROM UT.TEST_RUNS_LOG TRL
    INNER JOIN UT.TEST_RUNS_CONFIG TRC ON TRL.TEST_CASE_ID = TRC.TEST_CASE_ID
WHERE TRC.TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
    AND TRL.TEST_OUTCOME = 'FAIL'
    AND TRL.RUN_ID = (
        SELECT MAX(RUN_ID) 
        FROM UT.TEST_RUNS_LOG 
        WHERE TEST_CASE_ID IN (
            SELECT TEST_CASE_ID 
            FROM UT.TEST_RUNS_CONFIG 
            WHERE TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
        )
    )
ORDER BY TRL.TEST_CASE_ID;
```

### 8.3 Validate Test Coverage

```sql
-- Check test case coverage by type
SELECT 
    TEST_CASE_TYPE,
    COUNT(*) AS TOTAL_TESTS,
    SUM(CASE WHEN IS_ACTIVE = 1 THEN 1 ELSE 0 END) AS ACTIVE_TESTS
FROM UT.TEST_RUNS_CONFIG
WHERE TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
GROUP BY TEST_CASE_TYPE
ORDER BY TEST_CASE_TYPE;

-- Check parameter coverage
SELECT 
    OP.PARAM_NAME,
    OP.PARAM_DATATYPE,
    OP.IS_MANDATORY,
    COUNT(DISTINCT TPD.TEST_CASE_ID) AS TESTS_USING_PARAM,
    COUNT(DISTINCT CASE WHEN TPD.PARAM_VALUE IS NOT NULL THEN TPD.TEST_CASE_ID END) AS TESTS_WITH_VALUES
FROM UT.OBJECT_PARAM OP
    LEFT JOIN UT.TEST_PARAM_DATA TPD ON OP.PARAM_NAME = TPD.PARAM_NAME
        AND TPD.TEST_CASE_ID IN (
            SELECT TEST_CASE_ID 
            FROM UT.TEST_RUNS_CONFIG 
            WHERE OBJECT_ID = OP.OBJECT_ID
        )
WHERE OP.OBJECT_ID = 185
GROUP BY OP.PARAM_NAME, OP.PARAM_DATATYPE, OP.IS_MANDATORY, OP.PARAM_SEQ_NO
ORDER BY OP.PARAM_SEQ_NO;
```

### 8.4 Performance Analysis

```sql
-- Analyze test execution performance
SELECT 
    TRC.TEST_CASE_TYPE,
    COUNT(*) AS TEST_COUNT,
    AVG(DATEDIFF(MILLISECOND, TRL.START_TIME, TRL.END_TIME)) AS AVG_EXECUTION_MS,
    MIN(DATEDIFF(MILLISECOND, TRL.START_TIME, TRL.END_TIME)) AS MIN_EXECUTION_MS,
    MAX(DATEDIFF(MILLISECOND, TRL.START_TIME, TRL.END_TIME)) AS MAX_EXECUTION_MS
FROM UT.TEST_RUNS_LOG TRL
    INNER JOIN UT.TEST_RUNS_CONFIG TRC ON TRL.TEST_CASE_ID = TRC.TEST_CASE_ID
WHERE TRC.TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
    AND TRL.RUN_ID = (
        SELECT MAX(RUN_ID) 
        FROM UT.TEST_RUNS_LOG 
        WHERE TEST_CASE_ID IN (
            SELECT TEST_CASE_ID 
            FROM UT.TEST_RUNS_CONFIG 
            WHERE TEST_CASE_OBJECT = '[UT].[TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT]'
        )
    )
GROUP BY TRC.TEST_CASE_TYPE
ORDER BY TRC.TEST_CASE_TYPE;
```

---

## Examples of Complete Test Suites

### Example 1: Simple Procedure (1 Parameter)

**Procedure:** `USP_AHS_CMN_MANAGER_STAFF_GET`
- **Parameters:** 1 (@MEMBER_ID BIGINT)
- **Test Cases:** 15 (6 positive, 6 negative, 3 edge cases)
- **Files Generated:**
  - `USP_AHS_CMN_MANAGER_STAFF_GET_TestCases.sql`
  - `TEST_USP_AHS_CMN_MANAGER_STAFF_GET_DTD.sql`
  - `TEST_USP_AHS_CMN_MANAGER_STAFF_GET_UT.sql`
  - `USP_AHS_CMN_MANAGER_STAFF_GET_TEST_SUITE_README.md`

**Test Coverage:**
- Valid member IDs
- Invalid member IDs
- NULL values
- Boundary values (0, -1, MAX_VALUE)
- Non-existent member IDs

### Example 2: Complex JSON Parameter

**Procedure:** `USP_AHS_PP_AUTH_DUPLICATE_SERVICE_CODES_CHECK`
- **Parameters:** 1 (@PP_AUTH_DETAILS NVARCHAR(MAX) - JSON)
- **Test Cases:** 20 (7 positive, 8 negative, 5 edge cases)
- **Files Generated:**
  - `TEST_USP_AHS_PP_AUTH_DUPLICATE_SERVICE_CODES_CHECK.sql`

**Test Coverage:**
- Valid JSON with no duplicates
- Valid JSON with expected duplicates
- Invalid JSON format
- Empty JSON arrays
- Date overlap scenarios
- Modifier matching logic

### Example 3: Complex Multi-Parameter Procedure

**Procedure:** `USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT`
- **Parameters:** 18 (mixed types, optional/required)
- **Test Cases:** 15 (8 positive, 7 negative)
- **Files Generated:**
  - `USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_TestCases.sql`
  - `TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_INIT.sql`
  - `TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_DTD.sql`
  - `TEST_USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_UT.sql`
  - `USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT_TEST_SUITE_README.md`

**Test Coverage:**
- Pagination scenarios
- Sorting options
- Filter combinations
- Search modes
- Security flags
- Invalid parameters
- SQL injection attempts

---

## Troubleshooting

### Issue 1: MCP Server Won't Connect

**Symptoms:**
- Copilot Chat shows "MCP server not available"
- Connection timeout errors

**Solutions:**
1. Check `.vscode/mcp.json` configuration:
   ```json
   {
     "mcpServers": {
       "my-mcp-server": {
         "command": "python",
         "args": ["-u", "path/to/server.py"],
         "env": {
           "DB_SERVER": "your-server",
           "DB_NAME": "your-database"
         }
       }
     }
   }
   ```

2. Verify Python environment:
   ```powershell
   python --version
   pip list | findstr "pyodbc mcp"
   ```

3. Test database connectivity:
   ```powershell
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```

4. Check VS Code Output panel:
   - View → Output
   - Select "MCP" from dropdown
   - Look for error messages

### Issue 2: Missing Python Packages

**Symptoms:**
- ImportError: No module named 'aiohttp'
- ModuleNotFoundError: No module named 'mcp'

**Solutions:**
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install missing packages
pip install pyodbc
pip install mcp
pip install aiohttp
pip install python-dotenv

# Verify installation
pip list
```

### Issue 3: Database Connection Failures

**Symptoms:**
- "Login failed for user"
- "Cannot connect to database"
- ODBC driver errors

**Solutions:**
1. **Windows Authentication Issues:**
   ```json
   // In mcp.json, ensure these are empty for Windows Auth
   "DB_USER": "",
   "DB_PASSWORD": ""
   ```

2. **SQL Server Authentication:**
   ```json
   // Provide credentials
   "DB_USER": "your_username",
   "DB_PASSWORD": "your_password"
   ```

3. **Verify ODBC Driver:**
   ```powershell
   # Check installed drivers
   Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
   ```

4. **Test connection manually:**
   ```python
   import pyodbc
   conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=AHS-LP-945;Database=Ahs_Bit_Red_QA_8170;Trusted_Connection=yes;"
   conn = pyodbc.connect(conn_str)
   print("Connected successfully!")
   ```

### Issue 4: Linked Server Errors in UT

**Symptoms:**
- "Server 'AHS-LP-945' is not configured for RPC"
- "Could not find stored procedure"
- OPENQUERY errors

**Solutions:**
1. **Configure linked server for RPC:**
   ```sql
   EXEC sp_serveroption 'AHS-LP-945', 'rpc', 'true';
   EXEC sp_serveroption 'AHS-LP-945', 'rpc out', 'true';
   ```

2. **Verify linked server:**
   ```sql
   -- Check linked server exists
   EXEC sp_helpserver;
   
   -- Test linked server connection
   SELECT * FROM OPENQUERY([AHS-LP-945], 'SELECT @@VERSION');
   ```

3. **Alternative: Use local execution:**
   ```sql
   -- Instead of OPENQUERY, use direct execution
   EXEC [Ahs_Bit_Red_QA_8170].dbo.USP_PROCEDURE_NAME @Param = 'Value';
   ```

### Issue 5: Test Cases Fail with NULL Parameters

**Symptoms:**
- "Procedure expects parameter which was not supplied"
- NULL constraint violations

**Solutions:**
1. **In DTD procedure, check for NULL handling:**
   ```sql
   -- Provide fallback values
   IF @ValidHealthCoachID IS NULL
       SET @ValidHealthCoachID = 15894099;
   ```

2. **In UT procedure, handle NULL in SQL construction:**
   ```sql
   IF @ParamValue IS NULL OR @ParamValue = 'NULL'
       SET @Param_Concat = @Param_Concat + '@' + @ParamName + ' = NULL, ';
   ELSE
       SET @Param_Concat = @Param_Concat + '@' + @ParamName + ' = ''' + @ParamValue + ''', ';
   ```

3. **Verify TEST_PARAM_DATA has values:**
   ```sql
   SELECT * FROM UT.TEST_PARAM_DATA 
   WHERE TEST_CASE_ID = 2001 
   AND (PARAM_VALUE IS NULL OR PARAM_VALUE = '');
   ```

### Issue 6: #Actual Temp Table Column Mismatch

**Symptoms:**
- "The column was specified multiple times"
- "Invalid column name"
- INSERT/SELECT column mismatch errors

**Solutions:**
1. **Get actual procedure output:**
   ```sql
   -- Run procedure manually and analyze result set
   EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT
       @HEALTH_COACH_ID = 15894099,
       @PAGE_NUMBER = 1,
       @PAGE_SIZE = 1;
   ```

2. **Use sp_describe_first_result_set (if supported):**
   ```sql
   EXEC sp_describe_first_result_set 
       N'EXEC dbo.USP_AHS_CM_MY_CARE_MEMBER_LIST_GET_DEFAULT 
         @HEALTH_COACH_ID = 15894099, 
         @PAGE_NUMBER = 1, 
         @PAGE_SIZE = 1';
   ```

3. **Update #Actual table definition:**
   ```sql
   -- Match exact columns returned by procedure
   CREATE TABLE #Actual (
       -- Copy column list from procedure output
       COLUMN1 DATATYPE,
       COLUMN2 DATATYPE,
       -- ...
   );
   ```

### Issue 7: Performance Issues

**Symptoms:**
- Tests take too long to execute
- Timeout errors
- Memory issues

**Solutions:**
1. **Run specific test cases:**
   ```sql
   -- Instead of all tests
   EXEC UT.[TEST_USP_PROCEDURE] @TEST_CASE_ID = 2001, @debug = 2;
   ```

2. **Optimize DTD queries:**
   ```sql
   -- Use indexes and efficient queries
   SELECT TOP 1 @ValidID = MEMBER_ID
   FROM CARE_STAFF_DETAILS WITH (NOLOCK)
   WHERE STATUS_ID = 1
   ORDER BY MEMBER_ID;
   ```

3. **Limit data in positive tests:**
   ```sql
   -- Use small page sizes for testing
   @PAGE_SIZE = 10  -- Instead of 100
   ```

4. **Use debug mode 1 first:**
   ```sql
   -- Review SQL before executing
   EXEC UT.[TEST_USP_PROCEDURE] @TEST_CASE_ID = NULL, @debug = 1;
   ```

---

## Best Practices

### 1. MCP Server Configuration

✅ **Do:**
- Keep `mcp.json` in `.vscode` folder (workspace-specific)
- Use environment variables for sensitive data
- Set `PYTHONPATH` to include server directory
- Use absolute paths for `command` and `args`

❌ **Don't:**
- Commit passwords to version control
- Use relative paths in configuration
- Mix development and production configurations

### 2. Test Case Design

✅ **Do:**
- Cover all parameters (at least once)
- Test boundary values (0, 1, MAX, MIN)
- Include NULL scenarios
- Test parameter combinations
- Use realistic test data
- Document expected outcomes

❌ **Don't:**
- Test only "happy path"
- Ignore edge cases
- Use production data directly
- Hard-code all test values

### 3. INIT Procedure

✅ **Do:**
- Use unique @ObjectID for each procedure
- Increment @BaseTestCaseID by 100 for each new procedure
- Document parameter purposes
- Mark mandatory parameters correctly
- Sequence parameters logically

❌ **Don't:**
- Reuse Object IDs
- Skip parameter documentation
- Mix test case ID ranges

### 4. DTD Procedure

✅ **Do:**
- Query actual database for valid data
- Always provide fallback values
- Use NEWID() for randomization
- Filter by active/valid records
- Handle NULL gracefully
- Update only POSITIVE test cases

❌ **Don't:**
- Hard-code all values
- Assume data exists
- Update NEGATIVE test cases with valid data
- Use deleted/inactive records

### 5. UT Procedure

✅ **Do:**
- Call DTD before test execution
- Handle NULL parameters properly
- Log all test outcomes
- Provide detailed error messages
- Support multiple debug modes
- Generate summary reports
- Clean old test logs regularly

❌ **Don't:**
- Skip error handling
- Execute without DTD
- Ignore failed tests
- Mix test runs (use unique RUN_ID)

### 6. Naming Conventions

**Files:**
```
[ProcedureName]_TestCases.sql
TEST_[ProcedureName]_INIT.sql
TEST_[ProcedureName]_DTD.sql
TEST_[ProcedureName]_UT.sql
[ProcedureName]_TEST_SUITE_README.md
```

**Procedures:**
```sql
UT.[TEST_[ProcedureName]_INIT]
UT.[TEST_[ProcedureName]_DTD]
UT.[TEST_[ProcedureName]]  -- UT procedure
```

**Test Cases:**
```sql
TC_[TestCaseID]_[ShortDescription]
Example: TC_2001_BasicExecution
```

### 7. Version Control

✅ **Do:**
- Commit all generated files
- Use meaningful commit messages
- Tag test suite versions
- Document changes in README
- Keep test cases in templates folder

❌ **Don't:**
- Commit sensitive data
- Mix multiple procedures in one commit
- Skip documentation updates

### 8. Maintenance

✅ **Do:**
- Review test results regularly
- Update DTD when data changes
- Adjust tests when procedures change
- Archive old test logs
- Monitor test execution time
- Keep procedures in sync with application changes

❌ **Don't:**
- Let test suites become outdated
- Ignore failing tests
- Keep unnecessary test cases
- Accumulate old test logs indefinitely

### 9. Documentation

✅ **Do:**
- Create README for each test suite
- Document test case purposes
- Include setup instructions
- Provide troubleshooting tips
- List known issues
- Update documentation with changes

❌ **Don't:**
- Skip documentation
- Assume everything is self-explanatory
- Leave outdated information

### 10. Collaboration

✅ **Do:**
- Share test results with team
- Document failures clearly
- Review test cases in code reviews
- Coordinate test case ID ranges
- Use consistent standards across team

❌ **Don't:**
- Work in isolation
- Skip peer review
- Use conflicting test case IDs
- Ignore team standards

---

## Appendix A: Template Files Reference

### Available Templates

1. **TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_INIT.sql**
   - Template for INIT procedures
   - Complex multi-parameter example
   - 35 test cases

2. **TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD.sql**
   - Template for DTD procedures
   - Multiple dynamic queries
   - Fallback value patterns

3. **TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED_UT.sql**
   - Template for UT procedures
   - Complete execution framework
   - Debug mode implementation

### Template Selection Guide

| Procedure Complexity | Parameters | Recommended Template |
|---------------------|------------|---------------------|
| Simple | 1-3 | CARE_PLAN_REQUEST_RECEIVED |
| Moderate | 4-10 | CARE_PLAN_REQUEST_RECEIVED |
| Complex | 11+ | QUALITY_INDICATOR_DASHBOARD |

---

## Appendix B: Quick Reference Commands

### MCP Connection
```
@workspace connect to the mcp server
```

### Test Suite Generation Request
```
@workspace Review the SQL Server stored procedure named [PROCEDURE_NAME] and generate:
1. Test Cases: Provide at least 3 positive and 3 negative test cases
2. INIT Procedure using template TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_INIT.sql
3. DTD Procedure using template TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD.sql
4. UT Procedure using template TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED_UT.sql

Save all files to templates folder.
```

### Execution Commands
```sql
-- Initialize
EXEC UT.[TEST_USP_PROCEDURE_INIT] @BaseTestCaseID = [ID], @ObjectID = [ID];

-- Prepare Data
EXEC UT.[TEST_USP_PROCEDURE_DTD] @DEST_DB_NAME = 'DatabaseName';

-- Execute Tests
EXEC UT.[TEST_USP_PROCEDURE] @DEST_DB_NAME = 'DatabaseName', @SERVER_NAME = 'ServerName', @debug = 2;
```

### Validation Queries
```sql
-- Check INIT
SELECT * FROM UT.OBJECT_DETAILS WHERE OBJECT_ID = [ID];
SELECT * FROM UT.TEST_RUNS_CONFIG WHERE OBJECT_ID = [ID];

-- Check DTD
SELECT * FROM UT.TEST_PARAM_DATA WHERE TEST_CASE_ID = [ID];

-- Check UT Results
SELECT * FROM UT.TEST_RUNS_LOG WHERE RUN_ID = [RUN_ID];
```

---

## Appendix C: UT Schema DDL

### Required Tables

```sql
-- Object Details
CREATE TABLE UT.OBJECT_DETAILS (
    OBJECT_ID INT PRIMARY KEY,
    OBJECT_NAME NVARCHAR(255),
    OBJECT_PURPOSE_ID INT,
    OBJECT_TYPE_ID INT,
    OBJECT_DESCRIPTION NVARCHAR(MAX),
    SCHEMA_NAME NVARCHAR(50),
    IS_ACTIVE BIT,
    CREATED_BY INT,
    CREATED_DATE DATETIME,
    MODIFIED_BY INT,
    MODIFIED_DATE DATETIME
);

-- Object Parameters
CREATE TABLE UT.OBJECT_PARAM (
    OBJECT_PARAM_ID INT IDENTITY(1,1) PRIMARY KEY,
    OBJECT_ID INT,
    PARAM_SEQ_NO INT,
    PARAM_NAME NVARCHAR(255),
    PARAM_DATATYPE NVARCHAR(50),
    PARAM_LENGTH INT,
    IS_MANDATORY BIT,
    DEFAULT_VALUE NVARCHAR(MAX),
    PARAM_DESCRIPTION NVARCHAR(MAX),
    CREATED_BY INT,
    CREATED_DATE DATETIME,
    FOREIGN KEY (OBJECT_ID) REFERENCES UT.OBJECT_DETAILS(OBJECT_ID)
);

-- Test Configuration
CREATE TABLE UT.TEST_RUNS_CONFIG (
    TEST_CASE_ID INT PRIMARY KEY,
    OBJECT_ID INT,
    TEST_CASE_OBJECT NVARCHAR(500),
    TEST_CASE_NAME NVARCHAR(255),
    TEST_CASE_DESCRIPTION NVARCHAR(MAX),
    TEST_CASE_TYPE VARCHAR(16),
    IS_ACTIVE BIT,
    CREATED_BY INT,
    CREATED_DATE DATETIME,
    FOREIGN KEY (OBJECT_ID) REFERENCES UT.OBJECT_DETAILS(OBJECT_ID)
);

-- Test Parameter Data
CREATE TABLE UT.TEST_PARAM_DATA (
    TEST_PARAM_DATA_ID INT IDENTITY(1,1) PRIMARY KEY,
    TEST_CASE_ID INT,
    PARAM_SEQ_NO INT,
    PARAM_NAME NVARCHAR(255),
    PARAM_VALUE NVARCHAR(MAX),
    CREATED_BY INT,
    CREATED_DATE DATETIME,
    MODIFIED_BY INT,
    MODIFIED_DATE DATETIME,
    FOREIGN KEY (TEST_CASE_ID) REFERENCES UT.TEST_RUNS_CONFIG(TEST_CASE_ID)
);

-- Test Execution Log
CREATE TABLE UT.TEST_RUNS_LOG (
    TEST_RUN_LOG_ID INT IDENTITY(1,1) PRIMARY KEY,
    RUN_ID BIGINT,
    TEST_CASE_ID INT,
    START_TIME DATETIME,
    END_TIME DATETIME,
    TEST_OUTCOME NVARCHAR(50),
    ERROR_MESSAGE NVARCHAR(MAX),
    CREATED_BY INT,
    CREATED_DATE DATETIME,
    FOREIGN KEY (TEST_CASE_ID) REFERENCES UT.TEST_RUNS_CONFIG(TEST_CASE_ID)
);

-- Resource Details
CREATE TABLE UT.Resource_details (
    Resource_id INT PRIMARY KEY,
    USER_NAME NVARCHAR(255),
    DOMAIN_NAME NVARCHAR(255),
    FULL_NAME NVARCHAR(255)
);
```

---

## Support and Contact

For issues, questions, or suggestions regarding this test suite generation workflow:

- **Documentation:** Review this guide thoroughly
- **Troubleshooting:** See [Troubleshooting](#troubleshooting) section
- **Team Lead:** Contact your technical lead for process questions
- **Database Team:** Contact DBA team for database access issues

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Maintained By:** Development Team
