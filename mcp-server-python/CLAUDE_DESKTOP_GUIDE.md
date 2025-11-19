# 🤖 Claude Desktop + Your Database Setup Guide

## 🚀 Quick Setup (2 Steps)

### Step 1: Install Configuration
Double-click: `setup_claude_desktop.bat`
- This automatically configures Claude Desktop to use your database
- Creates backup of existing config
- No manual editing needed!

### Step 2: Verify Setup
Double-click: `verify_claude_config.bat`
- Checks all paths and settings
- Validates the configuration
- Tests server startup

## 🎯 Using Claude with Your Database

Once configured, restart Claude Desktop and try these prompts:

### 📊 **Explore Your Database**
```
"List all tables in my database"
"How many tables do I have?"
"Show me tables that contain 'PATIENT' in the name"
"What stored procedures are available?"
```

### 🔍 **Table Information**
```
"Show me the structure of the PATIENT_DETAILS table"
"Describe the CARE_STAFF_DETAILS table columns"
"What indexes exist on PATIENT_FOLLOWUP table?"
"Show me all columns in PATIENT_DETAILS that allow NULL values"
```

### 📈 **Data Queries**
```
"Count how many records are in PATIENT_DETAILS"
"Show me the first 10 patients from PATIENT_DETAILS"
"Find patients where DELETED_BY is null"
"Count active care staff members"
```

### 🔧 **Your Stored Procedure**
```
"Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET with LOGIN_USERID 68"
"Run the referrals stored procedure with page size 10"
"Show me what parameters USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET needs"
"Execute the referrals procedure and show me the first 5 results"
```

### 🔗 **Complex Queries**
```
"Join PATIENT_DETAILS with CARE_STAFF_DETAILS to show patient-staff relationships"
"Find all patient followups from the last 30 days"
"Show me patients assigned to care staff member ID 1786"
"Count followups by referral status"
```

### 📋 **Business Intelligence**
```
"What are the most common treatment types in my database?"
"Show me referral statistics by month"
"Which care staff members have the most patient assignments?"
"Analyze patient distribution by status"
```

## 🛠️ **Configuration Details**

Your Claude Desktop is configured with:
- **Server**: AHS-LP-945
- **Database**: Ahs_Bit_Red_QA_8170
- **Authentication**: Windows Authentication
- **Tables**: 1,815 available
- **Stored Procedures**: 6,064 available

## 🔧 **Troubleshooting**

### Issue: "MCP server not responding"
1. Run `verify_claude_config.bat` to check setup
2. Restart Claude Desktop
3. Ensure database server is running

### Issue: "Database connection failed"
1. Run `run_direct_test.bat` to verify database access
2. Check if SQL Server service is running
3. Verify Windows Authentication is working

### Issue: "No tools available"
1. Restart Claude Desktop completely
2. Check configuration with `verify_claude_config.bat`
3. Re-run `setup_claude_desktop.bat`

## 📱 **Mobile Usage**
Note: MCP servers only work with Claude Desktop, not Claude mobile apps or web version.

## 🔒 **Security**
- Uses Windows Authentication (no passwords stored)
- Read-only access recommended for AI queries
- Stored procedures can modify data - use carefully

## 🎉 **What You Can Do Now**

With 1,815 tables and 6,064 stored procedures accessible through natural language:

1. **Ask business questions** in plain English
2. **Explore data relationships** without writing SQL
3. **Generate reports** through conversation
4. **Monitor database health** with simple questions
5. **Execute complex procedures** with natural language

## 💡 **Pro Tips**

1. **Be specific**: "Show me the PATIENT_DETAILS table structure" works better than "show me tables"
2. **Use table names**: Claude knows your exact table names
3. **Ask for samples**: "Show me 5 example records" gives you data context
4. **Combine operations**: "List tables and count their records"
5. **Use your procedure**: Claude knows about USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET

---

**Ready to go!** Run the setup, restart Claude Desktop, and start asking questions about your 1,815 tables! 🚀