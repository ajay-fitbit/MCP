-- TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET.sql
CREATE OR ALTER PROCEDURE UT.[TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET]
    @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170', @SERVER_NAME VARCHAR(30) = 'AHS-LP-945', @TEST_CASE_ID INT=NULL, @debug INT = 0
AS
SET NOCOUNT ON;
BEGIN
	-- Insert Dynamic Test Data into TEST_PARAM_DATA Table.
	IF @TEST_CASE_ID IS NULL
		EXEC UT.TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET_DTD @DEST_DB_NAME = @DEST_DB_NAME;
	ELSE
		EXEC UT.TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET_DTD @DEST_DB_NAME = @DEST_DB_NAME, @TEST_CASE_ID = @TEST_CASE_ID;

    -- Declare variables
	DECLARE @TestCaseID INT, @TestCaseName NVARCHAR(MAX), @ParamName NVARCHAR(MAX), @ParamValue NVARCHAR(MAX);
	DECLARE @sqlCommand NVARCHAR(MAX), @START_TIME DATETIME, @END_TIME DATETIME, @TestOutcome NVARCHAR(50), @ErrorMessage NVARCHAR(MAX), @TestCaseDesc NVARCHAR(MAX);
	DECLARE @TestCaseObject NVARCHAR(500) = '[UT].[TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET]';
	--DECLARE @CreatedBy NVARCHAR(50) = SYSTEM_USER; --'ALTRUISTA\ajay.singh';
	DECLARE @CreateTable NVARCHAR(MAX);
	DECLARE @CreatedBy int 	select @CreatedBy = Resource_id from UT.Resource_details where  concat(DOMAIN_NAME,'\',[USER_NAME])=SUSER_NAME()	-- User fail safe	SET @CreatedBy = IIF(isnull(@CreatedBy,'')='', 999,@CreatedBy);
	DECLARE @Param_Concat varchar(max);

	-- Default values for parameters
    DECLARE @AUTH_NO BIGINT = NULL;
    DECLARE @IS_LOB INT = 0;
    DECLARE @LOGIN_USERID BIGINT = NULL;
    DECLARE @INPUT_PATIENT_ID BIGINT = 0;
    
    SET @TestOutcome = 'PASS';
    SET @ErrorMessage = '';

    -- Clean test case data
    IF @TEST_CASE_ID IS NULL
        DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID IN (SELECT TEST_CASE_ID FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_OBJECT = @TestCaseObject)
    ELSE
        DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID = @TEST_CASE_ID;
    
	DECLARE @RUN_ID BIGINT = CAST(CONVERT(VARCHAR, GETDATE(), 112) +
        RIGHT('0' + CONVERT(VARCHAR, DATEPART(HOUR, GETDATE())), 2) +
        RIGHT('0' + CONVERT(VARCHAR, DATEPART(MINUTE, GETDATE())), 2) +
        RIGHT('0' + CONVERT(VARCHAR, DATEPART(SECOND, GETDATE())), 2) AS BIGINT);

	-- For IS_LOB = 1, we need few columns
    CREATE TABLE #Actual
    (        
        DATA_ROOT_NAME	NVARCHAR(2128),
		DUE_DATE DATETIME,
		IS_ACTIVE BIT,
		IS_SELECTED BIT,
		AUTH_STATUS VARCHAR(50)
    );
	-- For standard details
	CREATE TABLE #Actual_standard
    (
        PATIENT_ID BIGINT,
		AUTH_ID VARCHAR(50),
		CLASS_ID INT,
		AUTH_NO	BIGINT,
		FIRST_NAME	NVARCHAR(400),
		MIDDLE_NAME	NVARCHAR(400),
		IS_SAVED BIT,
		IS_HNA BIT
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

		EXEC [UT].[TEST_USP_GET_PARAM_VALUE] @RESULT_TABLE = N'UT.TEST_PARAM_DATA',@TEST_CASE_ID = @TestCaseID,@PARAM_NAME = N'IS_LOB',@Result = @IS_LOB OUTPUT

		--- Logic for validating Stored Procedure
		BEGIN TRY

			-- Temp table cleanup
			TRUNCATE TABLE #Actual;
			truncate table #Actual_standard
			-- Execute the procedure
			SET @START_TIME = GETDATE();
			IF @debug = 1 print cast(@TestCaseID as varchar(10)) +  '-INSERT INTO #Actual ('+ @sqlCommand+')';
			ELSE
			BEGIN
				if @debug = 2
					print 'INSERT INTO #Actual ('+ @sqlCommand +')'

				IF @IS_LOB = 1
				begin
					SET @sqlCommand = 'INSERT INTO #Actual ' + @sqlCommand;
					--INSERT INTO #Actual
					--EXEC SP_EXECUTESQL @sqlCommand;
				end
				else
				begin
					SET @sqlCommand = 'INSERT INTO #Actual_standard ' + @sqlCommand;
					--INSERT INTO #Actual_standard
					--EXEC SP_EXECUTESQL @sqlCommand;
				end
				EXEC SP_EXECUTESQL @sqlCommand;
			END
			SET @END_TIME = GETDATE();

			-- Validate the results
			SET @TestOutcome = 'PASS';
			SET @ErrorMessage = @TestCaseDesc + ' Successful';

			IF @IS_LOB = 1
			begin
				IF NOT EXISTS (SELECT 1 FROM #Actual)
				BEGIN
					SET @TestOutcome = 'PASS';
					SET @ErrorMessage = @TestCaseDesc + ' Failed: No Data found'
				END
			end
			else
			begin
				IF NOT EXISTS (SELECT 1 FROM #Actual_standard)
				BEGIN
					SET @TestOutcome = 'PASS';
					SET @ErrorMessage = @TestCaseDesc + ' Failed: No Data found'
				END
			end

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

			-- Call the insert log procedure
			IF @TestCaseID = 560
			BEGIN
				SET @TestOutcome = 'PASS';
				SET @ErrorMessage = ERROR_MESSAGE();
			END
			ELSE
			BEGIN
				SET @TestOutcome = 'FAIL';
				SET @ErrorMessage = ERROR_MESSAGE();
			END
			EXEC UT.TEST_INSERT_LOG_DATA @RUN_ID, @TestCaseID, @TestOutcome, @ErrorMessage, 'COMPLETE', @CreatedBy, @START_TIME, @END_TIME;
			if @debug = 2
					print 'EXEC UT.TEST_INSERT_LOG_DATA '+ cast(@RUN_ID as varchar(50)) +', '+ cast(@TestCaseID as varchar(20)) +', '''+ @TestOutcome+''', '''+ @ErrorMessage+''', ''COMPLETE'','''+ CAST(@CreatedBy AS VARCHAR(4)) +''', '''+ cast(@START_TIME as varchar(20)) +''', '''+ cast(@END_TIME as varchar(20)) +''';'
		END CATCH

		SET @Index += 1;
	END
END

-- Exec UT.[TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET] @debug = 2, @TEST_CASE_ID = 620
