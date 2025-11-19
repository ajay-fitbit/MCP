-- =============================================
-- Unit Test for USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED
-- Author: Ajay Singh
-- Date: October 17, 2025
-- JIRA: GCACCEL-1263
-- =============================================

CREATE OR ALTER PROCEDURE [UT].[TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED]
    @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170', @SERVER_NAME VARCHAR(30) = 'AHS-LP-945', @TEST_CASE_ID INT=NULL, @debug INT = 2
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Insert Dynamic Test Data or call DTD procedure if needed
    IF @TEST_CASE_ID IS NULL
        -- Run all test cases
        EXEC UT.[TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED_DTD] @DEST_DB_NAME=@DEST_DB_NAME, @TEST_CASE_ID = NULL
    ELSE
        -- Run specific test case
        EXEC UT.[TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED_DTD] @DEST_DB_NAME=@DEST_DB_NAME, @TEST_CASE_ID = @TEST_CASE_ID

    -- Declare variables
    DECLARE @TestCaseID INT, @TestCaseName NVARCHAR(MAX), @ParamName NVARCHAR(MAX), @ParamValue NVARCHAR(MAX);
    DECLARE @sqlCommand NVARCHAR(MAX), @START_TIME DATETIME, @END_TIME DATETIME, @TestOutcome NVARCHAR(50), @ErrorMessage NVARCHAR(MAX), @TestCaseDesc NVARCHAR(MAX);
    DECLARE @TestCaseObject NVARCHAR(500) = '[UT].[TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED]';
    DECLARE @CreateTable NVARCHAR(MAX);
    DECLARE @CreatedBy int;
    select @CreatedBy = Resource_id from UT.Resource_details where concat(DOMAIN_NAME,'\',[USER_NAME])=SUSER_NAME()
    -- User fail safe
    SET @CreatedBy = IIF(isnull(@CreatedBy,'')='', 999,@CreatedBy);
    DECLARE @Param_Concat varchar(max);

    -- Clean test case data.
    IF @TEST_CASE_ID IS NULL
        DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID IN (SELECT TEST_CASE_ID FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_OBJECT = @TestCaseObject)
    ELSE
        DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID IN (SELECT TEST_CASE_ID FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @TEST_CASE_ID)

    DECLARE @RUN_ID BIGINT = CAST(FORMAT(GETDATE(), 'yyMMddHHmmss') AS bigint);

    -- Declare ActualResults Temporary Table - Modify this to match procedure output
    -- For accurate columns, run: python generate_temp_table.py "path/to/USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED.sql"
    CREATE TABLE #Actual (
		PATIENT_ID bigint,
		FIRST_NAME varchar(255),
		LAST_NAME varchar(255),
		PATIENT_NAME varchar(255),
		CARE_TEAM_CARE_PLAN_ID bigint,
		CARE_PLAN_ID bigint,
		CONDITION_NAME varchar(255),
		GOAL_GROUP_NAME varchar(255),
		GOAL_NAME varchar(255),
		INTERVENTION_NAME varchar(255),
		CONDITION_ID bigint,
		START_DATE datetime,
		END_DATE datetime,
		SOURCE varchar(255),
		IS_SENSITIVE_DIAGNOSIS bit,
		OPP_NAME varchar(255),
		IS_MEMBER_ACCESSIBLE bit,
		CUSTOM_COUNT int
	);

    -- Create Table variable to store selected test cases
    DECLARE @TestCases TABLE (
        RowNum INT IDENTITY(1,1),
        TEST_CASE_ID INT,
        OBJECT_NAME NVARCHAR(MAX),
        TEST_CASE_DESCRIPTION NVARCHAR(MAX)
    );
    
    -- Inserting Testcases into Table Variable
    INSERT INTO @TestCases (TEST_CASE_ID, OBJECT_NAME, TEST_CASE_DESCRIPTION)
    SELECT CONF.TEST_CASE_ID, OD.[OBJECT_NAME], CONF.TEST_CASE_DESCRIPTION
    FROM UT.TEST_RUNS_CONFIG CONF
        INNER JOIN UT.OBJECT_DETAILS OD ON CONF.[OBJECT_ID] = OD.[OBJECT_ID]
    WHERE CONF.TEST_CASE_OBJECT = @TestCaseObject
        AND (@TEST_CASE_ID IS NULL OR CONF.TEST_CASE_ID = @TEST_CASE_ID)
    ORDER BY TEST_CASE_ID;

    -- Looping through all the test cases
    DECLARE @Index INT = 1, @Total INT;
    SELECT @Total = COUNT(*) FROM @TestCases;
    
    WHILE @Index <= @Total
    BEGIN
        SELECT @TestCaseID = TEST_CASE_ID, 
            @TestCaseName = OBJECT_NAME, 
            @TestCaseDesc = TEST_CASE_DESCRIPTION 
        FROM @TestCases WHERE RowNum = @Index;
        
        -- Setup exec script as a string
        SET @sqlCommand = 'EXEC ' + @DEST_DB_NAME + '.' + @TestCaseName + ' ';
        SELECT @Param_Concat=[UT].[FN_GET_PARAMETER_SET](@TestCaseID)
        SET @sqlCommand = @sqlCommand + @Param_Concat;
        
        BEGIN TRY
            
            -- Temp table cleanup
            TRUNCATE TABLE #Actual;

            SET @START_TIME = GETDATE();
            IF @debug = 1 print cast(@TestCaseID as varchar(10)) +  '-INSERT INTO #Actual ('+ @sqlCommand+')';
            ELSE
            BEGIN
                if @debug = 2
                    print 'INSERT INTO #Actual ('+ @sqlCommand +')'

                INSERT INTO #Actual
                EXEC Query @Server = @SERVER_NAME, @query  = @sqlCommand
            END

            -- Test cases validation
            DECLARE @RowCount INT;
            SELECT @RowCount = COUNT(*) FROM #Actual;
            
            -- Different validation based on test case
            SET @TestOutcome = 'PASS';
            SET @ErrorMessage = @TestCaseDesc + ' Successful';

            IF NOT EXISTS (SELECT 1 FROM #Actual)
            BEGIN
                SET @TestOutcome = 'PASS';
                SET @ErrorMessage = @TestCaseDesc + ' Failed: No Data found'
            END
            
            SET @END_TIME = GETDATE();
            
            -- Call the insert log procedure
            IF @debug = 1 print 'EXEC UT.TEST_INSERT_LOG_DATA '+ cast(@TestCaseID as varchar(20)) +', '''+ @TestCaseDesc +''', '''+ @TestOutcome +''', '''+ @ErrorMessage +''', ''COMPLETE'','''+ CAST(@CreatedBy AS VARCHAR(4)) +''', '+ cast(@START_TIME as varchar(20)) +', '+ cast(@END_TIME as varchar(20));
            ELSE
            BEGIN
                EXEC UT.TEST_INSERT_LOG_DATA @RUN_ID, @TestCaseID, @TestOutcome, @ErrorMessage, 'COMPLETE',@CreatedBy, @START_TIME, @END_TIME;
                if @debug = 2
                    print 'EXEC UT.TEST_INSERT_LOG_DATA '+ cast(@RUN_ID as varchar(50)) +', '+ cast(@TestCaseID as varchar(20)) +', '''+ @TestOutcome+''', '''+ @ErrorMessage+''', ''COMPLETE'','''+ CAST(@CreatedBy AS VARCHAR(4)) +''', '''+ cast(@START_TIME as varchar(20)) +''', '''+ cast(@END_TIME as varchar(20)) +''';'
            END
        END TRY
        BEGIN CATCH
            SET @END_TIME = GETDATE();
            SET @TestOutcome = 'FAIL';
            SET @ErrorMessage = ERROR_MESSAGE();
            
            EXEC UT.TEST_INSERT_LOG_DATA @RUN_ID, @TestCaseID, @TestOutcome, @ErrorMessage, 'COMPLETE', @CreatedBy, @START_TIME, @END_TIME;
            if @debug = 2
                print 'EXEC UT.TEST_INSERT_LOG_DATA '+ cast(@RUN_ID as varchar(50)) +', '+ cast(@TestCaseID as varchar(20)) +', '''+ @TestOutcome+''', '''+ @ErrorMessage+''', ''COMPLETE'','''+ CAST(@CreatedBy AS VARCHAR(4)) +''', '''+ cast(@START_TIME as varchar(20)) +''', '''+ cast(@END_TIME as varchar(20)) +''';'
        END CATCH

        -- Move to the next test case
        SET @Index = @Index + 1;
    END

    DROP TABLE #Actual;
END;
-- EXEC [UT].[TEST_USP_AHS_CMN_CARE_PLAN_REQUEST_RECEIVED] @debug = 2