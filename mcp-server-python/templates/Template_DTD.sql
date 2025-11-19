-- TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD.sql
CREATE OR ALTER PROCEDURE UT.[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD]
    @DEST_DB_NAME NVARCHAR(50) = 'Ahs_Bit_Red_QA_8170', 
    @TEST_CASE_ID INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @CurrentDate DATETIME = CONVERT(VARCHAR(23), GETDATE(), 112)
    DECLARE @TestCaseObject NVARCHAR(500) = '[UT].[TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET]',
            @TestCaseID INT, 
            @TestCaseType VARCHAR(16) = 'POSITIVE';

    -- Create Table variable to store selected test cases
    DECLARE @TestCases TABLE
    (
        RowNum INT IDENTITY(1, 1),
        TEST_CASE_ID INT,
        TEST_CASE_TYPE VARCHAR(16)
    );

    INSERT INTO @TestCases (TEST_CASE_ID, TEST_CASE_TYPE)
    SELECT CONF.TEST_CASE_ID, CONF.TEST_CASE_TYPE
    FROM UT.TEST_RUNS_CONFIG CONF
        INNER JOIN UT.OBJECT_DETAILS OD ON CONF.[OBJECT_ID] = OD.[OBJECT_ID]
    WHERE CONF.TEST_CASE_OBJECT = @TestCaseObject
          AND (@TEST_CASE_ID IS NULL OR CONF.TEST_CASE_ID = @TEST_CASE_ID)
    ORDER BY TEST_CASE_ID;

    -- Looping through all the test cases
    DECLARE @Index INT = 1, @Total INT;
    SELECT @Total = COUNT(*) FROM @TestCases;

    IF @Total > 0
    BEGIN
        -- Declare variables for SQL commands
        DECLARE @sqlCommand NVARCHAR(MAX);
        DECLARE @paramDefinition NVARCHAR(500);
        
        -- Get a valid CARE_STAFF_ID from MEMBER_CARESTAFF
        DECLARE @ValidCareStaffID BIGINT;
        
        SET @sqlCommand = N'SELECT TOP 1 @CareStaffID = mc.CREATED_BY
        FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.MEMBER_CARESTAFF mc
        WHERE mc.CREATED_BY IS NOT NULL
          AND mc.IS_ACTIVE = 1
        GROUP BY mc.CREATED_BY
        ORDER BY COUNT(*) DESC';

        SET @paramDefinition = N'@CareStaffID BIGINT OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @CareStaffID = @ValidCareStaffID OUTPUT;

        -- If no valid CARE_STAFF_ID found, create a fallback
        IF @ValidCareStaffID IS NULL
            SET @ValidCareStaffID = 316;
            
        -- Get valid CONDITION_IDs (comma separated) from CPL_MANAGE_CONDITION
        DECLARE @ValidConditionIDs NVARCHAR(4000);
        
        SET @sqlCommand = N'SELECT TOP 3 @ConditionIDs = STRING_AGG(CAST(CONDITION_ID AS VARCHAR), '','')
        FROM (
            SELECT TOP 3 CONDITION_ID
            FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.CPL_MANAGE_CONDITION
            WHERE DELETED_BY IS NULL
            ORDER BY CONDITION_ID
        ) AS CondIds';

        SET @paramDefinition = N'@ConditionIDs NVARCHAR(4000) OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @ConditionIDs = @ValidConditionIDs OUTPUT;

        -- If no valid CONDITION_IDs found, create a fallback
        IF @ValidConditionIDs IS NULL
            SET @ValidConditionIDs = '1,2,3';
            
        -- Get valid RISK_CATEGORY_IDs (comma separated) from RISK_CATEGORY
        DECLARE @ValidRiskCategoryIDs NVARCHAR(4000);
        
        SET @sqlCommand = N'SELECT TOP 3 @RiskCategoryIDs = STRING_AGG(CAST(RISK_CATEGORY_ID AS VARCHAR), '','')
        FROM (
            SELECT TOP 3 RISK_CATEGORY_ID
            FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.RISK_CATEGORY
            WHERE DELETED_BY IS NULL
            ORDER BY RISK_CATEGORY_ID
        ) AS RiskIds';

        SET @paramDefinition = N'@RiskCategoryIDs NVARCHAR(4000) OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @RiskCategoryIDs = @ValidRiskCategoryIDs OUTPUT;

        -- If no valid RISK_CATEGORY_IDs found, create a fallback
        IF @ValidRiskCategoryIDs IS NULL
            SET @ValidRiskCategoryIDs = '5,6,7';
            
        -- Get valid INDICATOR_IDs (comma separated) from INDICATOR
        DECLARE @ValidIndicatorIDs NVARCHAR(4000);
        
        SET @sqlCommand = N'SELECT TOP 3 @IndicatorIDs = STRING_AGG(CAST(INDICATOR_ID AS VARCHAR), '','')
        FROM (
            SELECT TOP 3 INDICATOR_ID
            FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.INDICATOR
            WHERE DELETE_FLAG = 0
            ORDER BY INDICATOR_ID
        ) AS IndIds';

        SET @paramDefinition = N'@IndicatorIDs NVARCHAR(4000) OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @IndicatorIDs = @ValidIndicatorIDs OUTPUT;

        -- If no valid INDICATOR_IDs found, create a fallback
        IF @ValidIndicatorIDs IS NULL
            SET @ValidIndicatorIDs = '1,2,3';
            
        -- Get valid OPPORTUNITY_IDs (comma separated) from CPL_CONDITION_OPPORTUNITY
        DECLARE @ValidOpportunityIDs NVARCHAR(1000);
        
        SET @sqlCommand = N'SELECT TOP 3 @OpportunityIDs = STRING_AGG(CAST(OPPORTUNITY_ID AS VARCHAR), '','')
        FROM (
            SELECT TOP 3 OPPORTUNITY_ID
            FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.CPL_CONDITION_OPPORTUNITY
            WHERE DELETED_BY IS NULL
              AND IS_ACTIVE = 1
            GROUP BY OPPORTUNITY_ID
            ORDER BY OPPORTUNITY_ID
        ) AS OppIds';

        SET @paramDefinition = N'@OpportunityIDs NVARCHAR(1000) OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @OpportunityIDs = @ValidOpportunityIDs OUTPUT;

        -- If no valid OPPORTUNITY_IDs found, create a fallback
        IF @ValidOpportunityIDs IS NULL
            SET @ValidOpportunityIDs = '2,3,4';
            
        -- Get a single valid INDICATOR_ID for NUMERATOR_ID
        DECLARE @ValidNumeratorID INT;
        
        SET @sqlCommand = N'SELECT TOP 1 @NumeratorID = INDICATOR_ID
        FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.INDICATOR
        WHERE DELETE_FLAG = 0
        ORDER BY INDICATOR_ID';

        SET @paramDefinition = N'@NumeratorID INT OUTPUT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, @NumeratorID = @ValidNumeratorID OUTPUT;

        -- If no valid NUMERATOR_ID found, create a fallback
        IF @ValidNumeratorID IS NULL
            SET @ValidNumeratorID = 1;
            
        -- Get a different valid INDICATOR_ID for DENOMINATOR_ID
        DECLARE @ValidDenominatorID INT;
        
        SET @sqlCommand = N'SELECT TOP 1 @DenominatorID = INDICATOR_ID
        FROM ' + QUOTENAME(@DEST_DB_NAME) + '.dbo.INDICATOR
        WHERE DELETE_FLAG = 0
          AND INDICATOR_ID <> @NumeratorID
        ORDER BY INDICATOR_ID DESC';

        SET @paramDefinition = N'@DenominatorID INT OUTPUT, @NumeratorID INT';
        EXEC sp_executesql @sqlCommand, @paramDefinition, 
            @DenominatorID = @ValidDenominatorID OUTPUT, 
            @NumeratorID = @ValidNumeratorID;

        -- If no valid DENOMINATOR_ID found, create a fallback
        IF @ValidDenominatorID IS NULL
            SET @ValidDenominatorID = 2;
            
        -- Set default values for ALERT_ID and PROGRAM_ID (typically numeric IDs)
        DECLARE @ValidAlertID VARCHAR(100) = '1';
        DECLARE @ValidProgramID VARCHAR(100) = '1';
    END

    WHILE @Index <= @Total
    BEGIN
        SELECT @TestCaseID = TEST_CASE_ID, @TestCaseType = TEST_CASE_TYPE
        FROM @TestCases WHERE RowNum = @Index;

        -- Update parameters for POSITIVE test cases only
        IF @TestCaseType = 'POSITIVE'
        BEGIN
            -- Update CARE_STAFF_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'CARE_STAFF_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'CARE_STAFF_ID', 
                    @PARAM_VALUE = @ValidCareStaffID;

            -- Update IS_CASELOAD parameter (default to 1 for My Caseload)
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'IS_CASELOAD')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'IS_CASELOAD', 
                    @PARAM_VALUE = 1;

            -- Update CONDITION_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'CONDITION_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'CONDITION_ID', 
                    @PARAM_VALUE = @ValidConditionIDs;

            -- Update RISK_CATEGORY_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'RISK_CATEGORY_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'RISK_CATEGORY_ID', 
                    @PARAM_VALUE = @ValidRiskCategoryIDs;

            -- Update INDICATOR_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'INDICATOR_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'INDICATOR_ID', 
                    @PARAM_VALUE = @ValidIndicatorIDs;

            -- Update OPPERTUNITY_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'OPPERTUNITY_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'OPPERTUNITY_ID', 
                    @PARAM_VALUE = @ValidOpportunityIDs;

            -- Update ALERT_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'ALERT_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'ALERT_ID', 
                    @PARAM_VALUE = @ValidAlertID;

            -- Update PROGRAM_ID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'PROGRAM_ID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'PROGRAM_ID', 
                    @PARAM_VALUE = @ValidProgramID;

            -- Update NUMERATORID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'NUMERATORID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'NUMERATORID', 
                    @PARAM_VALUE = @ValidNumeratorID;

            -- Update DENOMINATORID parameter
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'DENOMINATORID')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'DENOMINATORID', 
                    @PARAM_VALUE = @ValidDenominatorID;

            -- Update IS_ALL_OPP parameter (default to 0)
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'IS_ALL_OPP')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'IS_ALL_OPP', 
                    @PARAM_VALUE = 0;

            -- Update IS_ALL_PGMS parameter (default to 0)
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'IS_ALL_PGMS')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'IS_ALL_PGMS', 
                    @PARAM_VALUE = 0;

            -- Update IS_ALL_INDS parameter (default to 0)
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'IS_ALL_INDS')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'IS_ALL_INDS', 
                    @PARAM_VALUE = 0;

            -- Update SHOW_ACTIVE_RECORDS parameter (default to 2 for all records)
            IF EXISTS (SELECT 1 FROM [UT].[TEST_PARAM_DATA] WHERE TEST_CASE_ID = @TestCaseID AND PARAM_NAME = 'SHOW_ACTIVE_RECORDS')
                EXEC [UT].[TEST_USP_UPDATE_CONFIG_PARAM_DATA] 
                    @TEST_CASE_ID = @TestCaseID, 
                    @PARAM_NAME = 'SHOW_ACTIVE_RECORDS', 
                    @PARAM_VALUE = 2;
        END

        SET @Index += 1;
    END
END

-- Example execution
-- EXEC UT.TEST_USP_AHS_CM_QUALITY_INDICATOR_DASHBOARD_GET_DTD @TEST_CASE_ID = NULL