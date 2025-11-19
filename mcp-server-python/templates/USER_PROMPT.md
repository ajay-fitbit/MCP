# User Request Template
connect to my-mcp-server-0d6da389 connect database
```
Review the SQL Server stored procedure named `USP_AHS_CM_MEMBER_REQUEST_RECEIVED_GET` and generate the following deliverables:
Perform the below tasks, one after another and do not mixup or overlap.

1. **Test Cases**:
   - Provide at least 15 **positive** and **negative** test cases, always use most common and important scenarios.
   - Format each test case as: `EXEC USP_AHS_CM_MEMBER_REQUEST_RECEIVED_GET @param1 = value1, @param2 = value2, ...`
   - Add a line before each case starting with "-- Case 1:" with the description
   - Always validate each test cases with valid data.
   - Do not use ALL the parameters when they are not the focus of the test or relevent.
   - Do not include SQL Injection and date validations test cases

2. **Test Data Preparation Procedures**:
   - Generate the following procedures using templates from the `templates` folder:
     - `Template_INIT.sql` → for test framework setup, and make sure that it is synchronized with the TestCases file.
     - `Template_DTD.sql` → for dynamic test data generation, follow strict template structure.
     - `Template_UT.sql` → for unit test execution, follow strict template structure.
   - Prefix these files with `TEST_` and Follow the naming convention as within the template files.
   - Do **not** use hardcoded test case IDs.
   - Use `ObjectID` starting from **13**.
   - Use base test case ID starting from **92**.
   
   **DTD Generation Requirements**:
   - **ALWAYS validate database tables** before generating DTD queries:
     - Use `mcp_my-mcp-server_describe_table` to check table schema
     - Verify column existence.
     - Confirm data types and nullable constraints
   - **Adjust queries based on actual schema**:
     - Never assume column existence without validation
   - **Test data retrieval must**:
     - Query actual database tables used by the stored procedure
     - Use appropriate WHERE clauses based on validated schema
     - Provide fallback values for all variables
     - Handle NULL results gracefully

3. **File Restrictions**:
   - Do **not** generate any additional files.
   - Specifically, do **not** create:
     - README documents
     - Summary documents
     - Any other auxiliary files

### 📦 Standard Deliverables
- ✅ INIT file (test framework setup)
- ✅ DTD file (dynamic test data procedure)  
- ✅ UT file (unit test execution procedure)
- ✅ TestCases file (manual test cases)
``

---