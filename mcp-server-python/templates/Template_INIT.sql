-- =============================================
-- Test Configuration Initialization for [dbo].[USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]
-- Author: Ajay Singh
-- Date: October 21, 2025
-- =============================================

DECLARE @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170'
BEGIN
    SET NOCOUNT ON;

    -- Step 1: Define existing ObjectID and available Base TestCaseID
    DECLARE @ObjectID INT = 174;
    DECLARE @BaseTestCaseID INT = 1785;
	DECLARE @JiraTicket NVARCHAR(15) = 'GCACCEL-1263';

    DECLARE @CreatedBy int
    select @CreatedBy = Resource_id from UT.Resource_details where concat(DOMAIN_NAME,'\',[USER_NAME])=SUSER_NAME()
    -- User fail safe
    SET @CreatedBy = IIF(isnull(@CreatedBy,'')='', 999,@CreatedBy);

    -- Step 2: Register the procedure in OBJECT_DETAILS if not exists
    IF NOT EXISTS (SELECT 1 FROM UT.OBJECT_DETAILS WHERE OBJECT_NAME = '[dbo].[USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]')
    BEGIN
        INSERT INTO UT.OBJECT_DETAILS (OBJECT_ID, OBJECT_NAME, OBJECT_PURPOSE_ID, CREATED_BY, CREATED_ON, IS_ACTIVE)
        VALUES (@ObjectID, '[dbo].[USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]', 1, @CreatedBy, GETDATE(), 1);
    END

    -- Step 3: Clean up existing test cases
    DELETE FROM [UT].[TEST_RUNS_LOG] WHERE TEST_CASE_ID IN (SELECT TEST_CASE_ID FROM UT.TEST_RUNS_CONFIG WHERE OBJECT_ID = @ObjectID)

    DELETE FROM UT.TEST_PARAM_DATA
    WHERE TEST_CASE_ID BETWEEN @BaseTestCaseID + 1 AND @BaseTestCaseID + 20;

    DELETE FROM UT.TEST_RUNS_CONFIG
    WHERE TEST_CASE_ID BETWEEN @BaseTestCaseID + 1 AND @BaseTestCaseID + 20;

	DELETE FROM UT.OBJECT_PARAM WHERE OBJECT_ID = @ObjectID;

	INSERT INTO UT.OBJECT_PARAM (
		OBJECT_ID, PARAM_SEQ_NO, PARAM_NAME, PARAM_DATATYPE,DEFAULT_VALUE, IS_MANDATORY_PARAM, CREATED_ON, CREATED_BY, MODIFIED_ON, MODIFIED_BY, IS_ACTIVE) 
	VALUES
		(@ObjectID, 1, 'CARE_STAFF_ID', 'BIGINT', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 2, 'IS_CASELOAD', 'TINYINT', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 3, 'CONDITION_ID', 'NVARCHAR(2000)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 4, 'RISK_CATEGORY_ID', 'NVARCHAR(2000)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 5, 'INDICATOR_ID', 'NVARCHAR(2000)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 6, 'OPPERTUNITY_ID', 'NVARCHAR(500)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 7, 'ALERT_ID', 'VARCHAR(100)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 8, 'PROGRAM_ID', 'VARCHAR(100)', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 9, 'NUMERATORID', 'INT', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 10, 'DENOMINATORID', 'INT', 'NULL', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 11, 'IS_ALL_OPP', 'BIT', '0 --0 any-1 all', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 12, 'IS_ALL_PGMS', 'BIT', '0--0 any 1 all', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 13, 'IS_ALL_INDS', 'BIT', '0--0 any 1 all', 0, GETDATE(), @CreatedBy, NULL, NULL, 1),
		(@ObjectID, 14, 'SHOW_ACTIVE_RECORDS', 'TINYINT', '2', 0, GETDATE(), @CreatedBy, NULL, NULL, 1);

    -- Step 4: Define Test Cases
    INSERT INTO UT.TEST_RUNS_CONFIG (
        TEST_CASE_ID, OBJECT_ID, TEST_CASE_OBJECT, TEST_CASE_DESCRIPTION,
        TEST_CASE_SEQ_NO, TEST_CASE_TYPE, EXPECTED_RESULT, TEST_RESULT_MESSAGE,
        JIRA_ID, CREATED_BY, CREATED_ON, IS_ACTIVE
    )
    VALUES
        (@BaseTestCaseID + 1, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Basic execution with mandatory parameters only (My Caseload)', 1, 'POSITIVE', 'PASS', 'Basic execution with mandatory parameters only (My Caseload)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 2, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Basic execution with mandatory parameters (All Members)', 2, 'POSITIVE', 'PASS', 'Basic execution with mandatory parameters (All Members)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 3, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Basic execution with mandatory parameters (Other Members)', 3, 'POSITIVE', 'PASS', 'Basic execution with mandatory parameters (Other Members)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 4, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With single INDICATOR_ID filter', 4, 'POSITIVE', 'PASS', 'With single INDICATOR_ID filter',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 5, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With multiple INDICATOR_IDs (comma separated)', 5, 'POSITIVE', 'PASS', 'With multiple INDICATOR_IDs (comma separated)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 6, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With single RISK_CATEGORY_ID filter', 6, 'POSITIVE', 'PASS', 'With single RISK_CATEGORY_ID filter',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 7, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With multiple RISK_CATEGORY_IDs', 7, 'POSITIVE', 'PASS', 'With multiple RISK_CATEGORY_IDs',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 8, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With NUMERATORID and DENOMINATORID', 8, 'POSITIVE', 'PASS', 'With NUMERATORID and DENOMINATORID',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 9, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With SHOW_ACTIVE_RECORDS = 0 (Filtered - Active Only)', 9, 'POSITIVE', 'PASS', 'With SHOW_ACTIVE_RECORDS = 0 (Filtered - Active Only)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 10, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With SHOW_ACTIVE_RECORDS = 1 (Filtered - Inactive Only)', 10, 'POSITIVE', 'PASS', 'With SHOW_ACTIVE_RECORDS = 1 (Filtered - Inactive Only)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 11, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With IS_ALL_OPP = 1 (All Opportunities)', 11, 'POSITIVE', 'PASS', 'With IS_ALL_OPP = 1 (All Opportunities)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 12, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With IS_ALL_PGMS = 1 (All Programs)', 12, 'POSITIVE', 'PASS', 'With IS_ALL_PGMS = 1 (All Programs)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 13, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With IS_ALL_INDS = 1 (All Indicators)', 13, 'POSITIVE', 'PASS', 'With IS_ALL_INDS = 1 (All Indicators)',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Complex filter - Multiple parameters combined', 14, 'POSITIVE', 'PASS', 'Complex filter - Multiple parameters combined',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'All boolean flags set to 1', 15, 'POSITIVE', 'PASS', 'All boolean flags set to 1',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 16, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Different care staff with SHOW_ACTIVE_RECORDS = 2', 16, 'POSITIVE', 'PASS', 'Different care staff with SHOW_ACTIVE_RECORDS = 2',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 17, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With OPPERTUNITY_ID filter', 17, 'POSITIVE', 'PASS', 'With OPPERTUNITY_ID filter',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 18, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With ALERT_ID filter', 18, 'POSITIVE', 'PASS', 'With ALERT_ID filter',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 19, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'With PROGRAM_ID filter', 19, 'POSITIVE', 'PASS', 'With PROGRAM_ID filter',
        @JiraTicket, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, @ObjectID, '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
        'Maximum complexity - All parameters provided', 20, 'POSITIVE', 'PASS', 'Maximum complexity - All parameters provided',
        @JiraTicket, @CreatedBy, GETDATE(), 1);

    INSERT INTO [UT].[TEST_PARAM_DATA] (
        TEST_CASE_ID, PARAM_NAME, PARAM_VALUE, PARAM_SEQUENCE_NO, CREATED_BY, CREATED_ON, IS_ACTIVE
    )
    VALUES
    -- Parameters for Test Case 1: Basic execution with mandatory parameters only (My Caseload)
        (@BaseTestCaseID + 1, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 1, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 2: Basic execution with mandatory parameters (All Members)
        (@BaseTestCaseID + 2, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 2, 'IS_CASELOAD', '0', 2, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 3: Basic execution with mandatory parameters (Other Members)
        (@BaseTestCaseID + 3, 'CARE_STAFF_ID', '127694', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 3, 'IS_CASELOAD', '2', 2, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 4: With single INDICATOR_ID filter
        (@BaseTestCaseID + 4, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 4, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 4, 'INDICATOR_ID', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 5: With multiple INDICATOR_IDs (comma separated)
        (@BaseTestCaseID + 5, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 5, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 5, 'INDICATOR_ID', '1,2,3', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 6: With single RISK_CATEGORY_ID filter
        (@BaseTestCaseID + 6, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 6, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 6, 'RISK_CATEGORY_ID', '5', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 7: With multiple RISK_CATEGORY_IDs
        (@BaseTestCaseID + 7, 'CARE_STAFF_ID', '127694', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 7, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 7, 'RISK_CATEGORY_ID', '5,6,7', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 8: With NUMERATORID and DENOMINATORID
        (@BaseTestCaseID + 8, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 8, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 8, 'NUMERATORID', '1', 3, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 8, 'DENOMINATORID', '2', 4, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 9: With SHOW_ACTIVE_RECORDS = 0 (Filtered - Active Only)
        (@BaseTestCaseID + 9, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 9, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 9, 'SHOW_ACTIVE_RECORDS', '0', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 10: With SHOW_ACTIVE_RECORDS = 1 (Filtered - Inactive Only)
        (@BaseTestCaseID + 10, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 10, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 10, 'SHOW_ACTIVE_RECORDS', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 11: With IS_ALL_OPP = 1 (All Opportunities)
        (@BaseTestCaseID + 11, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 11, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 11, 'IS_ALL_OPP', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 12: With IS_ALL_PGMS = 1 (All Programs)
        (@BaseTestCaseID + 12, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 12, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 12, 'IS_ALL_PGMS', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 13: With IS_ALL_INDS = 1 (All Indicators)
        (@BaseTestCaseID + 13, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 13, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 13, 'IS_ALL_INDS', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 14: Complex filter - Multiple parameters combined
        (@BaseTestCaseID + 14, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'INDICATOR_ID', '1,2', 3, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'RISK_CATEGORY_ID', '5,6', 4, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'IS_ALL_OPP', '0', 5, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'IS_ALL_PGMS', '0', 6, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 14, 'SHOW_ACTIVE_RECORDS', '2', 7, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 15: All boolean flags set to 1
        (@BaseTestCaseID + 15, 'CARE_STAFF_ID', '758', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, 'IS_ALL_OPP', '1', 3, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, 'IS_ALL_PGMS', '1', 4, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, 'IS_ALL_INDS', '1', 5, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 15, 'SHOW_ACTIVE_RECORDS', '2', 6, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 16: Different care staff with SHOW_ACTIVE_RECORDS = 2
        (@BaseTestCaseID + 16, 'CARE_STAFF_ID', '127694', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 16, 'IS_CASELOAD', '0', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 16, 'SHOW_ACTIVE_RECORDS', '2', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 17: With OPPERTUNITY_ID filter
        (@BaseTestCaseID + 17, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 17, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 17, 'OPPERTUNITY_ID', '1,2,3', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 18: With ALERT_ID filter
        (@BaseTestCaseID + 18, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 18, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 18, 'ALERT_ID', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 19: With PROGRAM_ID filter
        (@BaseTestCaseID + 19, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 19, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 19, 'PROGRAM_ID', '1', 3, @CreatedBy, GETDATE(), 1),

    -- Parameters for Test Case 20: Maximum complexity - All parameters provided
        (@BaseTestCaseID + 20, 'CARE_STAFF_ID', '316', 1, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'IS_CASELOAD', '1', 2, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'CONDITION_ID', '1,2', 3, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'RISK_CATEGORY_ID', '5,6', 4, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'INDICATOR_ID', '1,2,3', 5, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'OPPERTUNITY_ID', '1', 6, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'ALERT_ID', '1', 7, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'PROGRAM_ID', '1', 8, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'NUMERATORID', '1', 9, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'DENOMINATORID', '2', 10, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'IS_ALL_OPP', '0', 11, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'IS_ALL_PGMS', '0', 12, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'IS_ALL_INDS', '0', 13, @CreatedBy, GETDATE(), 1),
        (@BaseTestCaseID + 20, 'SHOW_ACTIVE_RECORDS', '2', 14, @CreatedBy, GETDATE(), 1);
END;