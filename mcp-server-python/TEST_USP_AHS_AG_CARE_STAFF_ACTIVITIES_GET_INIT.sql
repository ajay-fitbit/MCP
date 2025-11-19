-- Initialize test configuration for USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET tests with multiple test cases

--CREATE OR ALTER PROCEDURE UT.INIT_TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET
  Declare  @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170'
--AS
BEGIN
    SET NOCOUNT ON;

	-- Get the Object ID for the stored procedure
	DECLARE @ObjectID INT = 110;
    -- Set base test case ID
    DECLARE @BaseTestCaseID INT = 923;

    DECLARE @CreatedBy INT
    SELECT @CreatedBy = Resource_id FROM UT.Resource_details WHERE CONCAT(DOMAIN_NAME,'\',[USER_NAME])=SUSER_NAME()
    -- User fail safe
    SET @CreatedBy = IIF(ISNULL(@CreatedBy,'')='', 999,@CreatedBy);

	-- Register the procedure in OBJECT_DETAILS if not exists
    IF NOT EXISTS (SELECT 1 FROM UT.OBJECT_DETAILS WHERE OBJECT_NAME = '[dbo].[USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]')
    BEGIN
        INSERT INTO UT.OBJECT_DETAILS (OBJECT_ID, OBJECT_NAME, OBJECT_PURPOSE_ID, CREATED_BY, CREATED_ON, IS_ACTIVE)
        VALUES (@ObjectID, '[dbo].[USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 1, @CreatedBy, GETDATE(), 1);
    END
    
    -- Clean up existing test cases
    DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID IN (SELECT TEST_CASE_ID FROM UT.TEST_RUNS_CONFIG WHERE OBJECT_ID = @ObjectID)
    
    -- Delete existing parameters for these test cases to avoid duplicates
    DELETE FROM UT.TEST_RUNS_CONFIG 
    WHERE TEST_CASE_ID BETWEEN @BaseTestCaseID + 1 AND @BaseTestCaseID + 11;

	-- Delete existing parameters for these test cases to avoid duplicates
    DELETE FROM UT.TEST_PARAM_DATA 
    WHERE TEST_CASE_ID BETWEEN @BaseTestCaseID + 1 AND @BaseTestCaseID + 11;

    -- Test Case 1: Default - Get staff activities with default parameters
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 1)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 1, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Basic Parameters',
            1, 'POSITIVE', 'PASS', 'Should return care staff activities with valid staff ID and request mode',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 2: Get staff activities with paging and sorting
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 2)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 2, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Paging and Sorting',
            2, 'POSITIVE', 'PASS', 'Should return care staff activities with paging and sorting',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 3: Invalid staff ID
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 3)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 3, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Invalid Staff ID',
            3, 'NEGATIVE', 'PASS', 'Should handle invalid staff ID gracefully',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 4: With Member Name and Altruista ID filters
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 4)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 4, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Member Name and Altruista ID Filters',
            4, 'POSITIVE', 'PASS', 'Should return care staff activities filtered by member name and altruista ID',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 5: Dashboard expanded with Current Date
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 5)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 5, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Dashboard Expanded and Current Date',
            5, 'POSITIVE', 'PASS', 'Should return care staff activities with dashboard expanded and current date',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 6: With Sensitive Records Viewing
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 6)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 6, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Sensitive Records Viewing',
            6, 'POSITIVE', 'PASS', 'Should return care staff activities including sensitive records',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 7: With COI Login User ID
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 7)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 7, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with COI Login User ID',
            7, 'POSITIVE', 'PASS', 'Should return care staff activities with COI login user ID',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 8: Date Range Variations - Future Date Range
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 8)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 8, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Future Date Range',
            8, 'POSITIVE', 'PASS', 'Should return care staff activities for the future date range',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 9: Dashboard Mode Combinations
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 9)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 9, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Dashboard Mode Combinations',
            9, 'POSITIVE', 'PASS', 'Should return care staff activities with various dashboard mode combinations',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 10: Special Character Handling
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 10)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 10, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Special Character Handling',
            10, 'POSITIVE', 'PASS', 'Should return care staff activities with special character handling',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Test Case 11: Order By and Sort Testing
    IF NOT EXISTS (SELECT 1 FROM UT.TEST_RUNS_CONFIG WHERE TEST_CASE_ID = @BaseTestCaseID + 11)
    BEGIN
        INSERT INTO UT.TEST_RUNS_CONFIG (
            TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION, 
            TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE, 
            JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
        )
        VALUES (
            @BaseTestCaseID + 11, @ObjectID, '[UT].[TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET]', 
            'Get Care Staff Activities with Order By and Sort Testing',
            11, 'POSITIVE', 'PASS', 'Should return care staff activities with order by and sort testing',
            'GCACCEL-1263', @CreatedBy, GETDATE(), 1
        );
    END
    
    -- Insert initial parameter values for all test cases using a single INSERT statement
    -- Updated to match the parameters of USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET
    INSERT INTO UT.TEST_PARAM_DATA (TEST_CASE_ID, PARAM_NAME, PARAM_VALUE, PARAM_SEQUENCE_NO, IS_ACTIVE, CREATED_BY, CREATED_ON)
    VALUES
        -- Test Case 1: Basic parameters
        (@BaseTestCaseID + 1, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'IS_FROM_DASHBOARD', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'PAGE_NUMBER', '1', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'PAGE_SIZE', '10', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'ORDER_BY_FIELD', 'ACTION_DATE', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'SORT_ORDER', 'ASC', 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 1, 'CS_VIEW_SENSITIVE', '0', 8, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 2: With paging and sorting
        (@BaseTestCaseID + 2, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'ORDER_BY_FIELD', 'PATIENT_NAME', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'SORT_ORDER', 'DESC', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'CS_VIEW_SENSITIVE', '0', 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'FROM_DATE', CONVERT(VARCHAR(10), DATEADD(DAY, -30, GETDATE()), 120), 8, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'TO_DATE', CONVERT(VARCHAR(10), GETDATE(), 120), 9, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'IS_FROM_DASHBOARD', '0', 10, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 2, 'IS_DASHBOARD_EXPANDED', '0', 11, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 3: Invalid staff ID
        (@BaseTestCaseID + 3, 'LOGIN_CARE_STAFF', '-1', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 3, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 3, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 3, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 3, 'ORDER_BY_FIELD', 'ACTION_DATE', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 3, 'SORT_ORDER', 'ASC', 6, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 4: With Member Name and Altruista ID filters
        (@BaseTestCaseID + 4, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'IS_FROM_DASHBOARD', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'MEMBER_NAME', 'Test Member', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'ALTRUISTA_ID', 'A12345', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'PAGE_NUMBER', '1', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'PAGE_SIZE', '10', 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'ORDER_BY_FIELD', 'ACTION_DATE', 8, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'SORT_ORDER', 'ASC', 9, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 4, 'CS_VIEW_SENSITIVE', '0', 10, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 5: Dashboard expanded with Current Date
        (@BaseTestCaseID + 5, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'IS_FROM_DASHBOARD', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'IS_DASHBOARD_EXPANDED', '1', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'CURRENT_DATE', CONVERT(VARCHAR(23), GETDATE(), 121), 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'PAGE_NUMBER', '1', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'PAGE_SIZE', '10', 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'ORDER_BY_FIELD', 'ACTION_DATE', 8, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 5, 'SORT_ORDER', 'ASC', 9, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 6: With Sensitive records viewing
        (@BaseTestCaseID + 6, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'CS_VIEW_SENSITIVE', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'PAGE_NUMBER', '1', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'PAGE_SIZE', '10', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'ORDER_BY_FIELD', 'ACTION_DATE', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 6, 'SORT_ORDER', 'ASC', 7, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 7: With COI_LOGIN_USER_ID
        (@BaseTestCaseID + 7, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'COI_LOGIN_USER_ID', '309', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'PAGE_NUMBER', '1', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'PAGE_SIZE', '10', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'ORDER_BY_FIELD', 'ACTION_DATE', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 7, 'SORT_ORDER', 'ASC', 7, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 8: Date Range Variations - Future Date Range
        (@BaseTestCaseID + 8, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'ORDER_BY_FIELD', 'ACTION_DATE', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'SORT_ORDER', 'ASC', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'FROM_DATE', CONVERT(VARCHAR(10), GETDATE(), 120), 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 8, 'TO_DATE', CONVERT(VARCHAR(10), DATEADD(MONTH, 3, GETDATE()), 120), 8, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 9: Dashboard Mode Combinations
        (@BaseTestCaseID + 9, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'ORDER_BY_FIELD', 'ACTION_DATE', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'SORT_ORDER', 'ASC', 6, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'IS_FROM_DASHBOARD', '0', 7, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'IS_DASHBOARD_EXPANDED', '1', 8, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 9, 'CURRENT_DATE', CONVERT(VARCHAR(23), GETDATE(), 121), 9, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 10: Special Character Handling
        (@BaseTestCaseID + 10, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 10, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 10, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 10, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 10, 'ORDER_BY_FIELD', 'ACTION_DATE', 5, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 10, 'SORT_ORDER', 'ASC', 6, 1, @CreatedBy, GETDATE()),
        
        -- Test Case 11: Order By and Sort Testing
        (@BaseTestCaseID + 11, 'LOGIN_CARE_STAFF', '309', 1, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 11, 'ACTION_DETAILS_ID', NULL, 2, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 11, 'PAGE_NUMBER', '1', 3, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 11, 'PAGE_SIZE', '10', 4, 1, @CreatedBy, GETDATE()),
        (@BaseTestCaseID + 11, 'ORDER_BY_FIELD', 'PATIENT_ID', 5, 1, @CreatedBy, GETDATE()),  -- Different ORDER_BY_FIELD
        (@BaseTestCaseID + 11, 'SORT_ORDER', 'DESC', 6, 1, @CreatedBy, GETDATE());    

    PRINT 'Test cases for USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET initialized successfully.';
END
GO
