# 🛡️ VISTA – Vulnerability Inspection & Security Tracking for AWS

VISTA is a comprehensive security assessment tool designed to scan AWS environments for potential security vulnerabilities and misconfigurations. It provides an intuitive visual interface to analyze security findings, view severity distributions, and implement recommended remediations.

## Features

- **Automated Security Scanning**: Scan AWS environments using access credentials
- **Vulnerability Validation**: Validates detected issues to determine actual exploitability
- **Interactive Dashboard**: Visual representation of findings with severity-based categorization
- **Detailed Reports**: Comprehensive security assessment reports with actionable remediation steps
- **Historical Data**: Track and compare security posture over time with previous scan results

## Dashboard Components

### Home Page

The home page serves as the landing page with an overview of the tool's capabilities:

- Welcome message introducing the AWS RedTeam Dashboard
- Three feature cards highlighting key functionalities:
    - Comprehensive Scanning: Scanning AWS environments for security vulnerabilities
    - Detailed Reports: Actionable remediation steps
    - Validation Testing: Elimination of false positives
- Primary "Start New Security Assessment" button
- Secondary "View Previous Assessments" link
- Consistent navigation header for Home, Previous Scans, and New Scan

### New Scan Page

The scan initiation page provides a simple interface to start security assessments:

- Input fields for AWS Access Key ID and Secret Access Key
- Region selection dropdown (defaulting to US East N. Virginia)
- "Schedule Security Assessment" button to initiate the scan
- Clear instructions for credential usage

### Previous Scans

The dashboard maintains a comprehensive history of all security assessments:

- Tabular view with sortable columns
- Scan ID (with unique identifiers formatted as scan-YYYYMMDD-HHMMSS)
- Date and time of scan
- AWS region scanned
- Number of findings
- Scan status (completed/in progress)
- "View" action buttons for accessing detailed results
- "New Scan" and "Refresh" buttons for easy navigation

### Results Dashboard

After selecting a scan from the Previous Scans page, the dashboard displays:

- Summary cards showing total issues and breakdown by severity (High, Medium, Low)
- Pie chart visualization of vulnerabilities by severity
- Tabular display of top findings by type
- Detailed findings with validation status (Exploitable/Not Exploitable in Practice)

### Findings Detail

Each finding includes:

- Severity classification
- Description of the security issue
- Validation status and evidence
- Step-by-step remediation instructions
- Potential impact assessment
- Priority order for remediation

## Architecture

The AWS Red Team Dashboard operates with a serverless architecture consisting of several key components:

### Frontend

- **Web Interface**: HTML/CSS/JavaScript hosted on Amazon S3
- **Visualization**: Chart.js for graphical representation of security findings
- **Responsive Design**: Bootstrap framework for responsive layout and UI components

![AWSRedTeamTool.png](AWSRedTeamTool.png)

### Authentication & Security

- **User Authentication**: Amazon Cognito for secure user authentication and session management
- **API Security**: API endpoints with proper IAM roles and policies

### Backend Components

- **AWS Lambda Functions**:
    1. **aws-redteam-scanner**: Primary scanning function that:
        - Analyzes AWS configuration using credentials provided by the user
        - Processes findings through a LangGraph workflow for intelligent analysis
        - Validates potential issues for exploitability
        - Stores results in DynamoDB for persistence
    2. **aws-redteam-get-results**: Results retrieval function that:
        - Queries DynamoDB for specific scan results
        - Formats findings for dashboard display
        - Generates comprehensive security reports
    3. **aws-redteam-listscan**: Scan history function that:
        - Lists all previous security assessments
        - Returns metadata about past scans (time, region, finding count)
        - Enables historical comparison of security posture
- **API Gateway**: RESTful API endpoints mapped to Lambda functions:
    - `/scan`: Initiates new security assessments
    - `/results`: Retrieves scan results by ID
    - `/list`: Gets history of previous scans
- **Database**: Amazon DynamoDB for storing:
    - Security scan results
    - Finding details and validation status
    - Remediation recommendations

### IAM Roles and Permissions

The Lambda functions use specific IAM roles with read-only permissions to safely analyze AWS environments for security vulnerabilities:

- **IAM User Assessment Permissions**:
    - `iam:GetLoginProfile`: Evaluates if users have console access
    - `iam:GetAccountPasswordPolicy`: Reviews password policy compliance
    - `iam:GetAccessKeyLastUsed`: Identifies potentially dormant access keys
    - `iam:ListUserPolicies`: Examines direct policy attachments
    - `iam:ListGroupsForUser`: Maps user-to-group relationships
    - `iam:ListAttachedUserPolicies`: Reviews managed policies attached to users
    - `iam:ListAttachedGroupPolicies`: Examines policies attached to groups
    - `iam:ListMFADevices`: Identifies users without MFA enabled
    - `iam:ListAccessKeys`: Discovers access keys for rotation compliance
    - `iam:ListUsers`: Enumerates all IAM users for assessment
- **DynamoDB Permissions**: Lambda functions have permissions to read/write scan results to DynamoDB tables with the prefix `aws-redteam-*`
- **CloudWatch Logs Permissions**: Standard logging permissions for Lambda function monitoring and troubleshooting

These targeted IAM permissions ensure the tool has sufficient access to perform thorough security assessments while adhering to the principle of least privilege.

## Security Assessment Capabilities

The dashboard can identify and validate various AWS security issues, including:

- IAM misconfigurations (e.g., users without MFA)
- Security group vulnerabilities (e.g., overly permissive rules)
- Public exposure of sensitive resources
- Excessive permissions and privilege escalation paths

## Getting Started

### Prerequisites

- AWS Account
- Web browser
- AWS credentials with appropriate permissions to scan resources


### Running a Security Assessment

1. Click "Start New Security Assessment" on the home page or "New Scan" in the navigation
2. Enter your AWS Access Key ID
3. Enter your AWS Secret Access Key
4. Select the target AWS region from the dropdown
5. Click "Schedule Security Assessment"

### Viewing Results

Due to Lambda computation limitations, results cannot be viewed in real-time. Instead:

1. Navigate to the "Previous Scans" section after initiating a scan
2. Locate your scan in the table (newest scans appear at the top)
3. Once the status shows "completed", click the "View" button
4. Review the summary of findings including severity breakdown
5. Examine detailed findings and remediation recommendations

### Navigation Flow

The dashboard is designed with a specific flow to accommodate Lambda's computation limitations:

1. Home page → Overview and quick access to main functions
2. New Scan → Input credentials and initiate assessment
3. Previous Scans → View history and access completed reports
4. Results View → Accessed from Previous Scans to see detailed findings

This navigation pattern ensures users can access comprehensive results while working within AWS service constraints.

## Security Considerations

- AWS credentials are used only for scanning and are not stored permanently
- Authentication is required to access the dashboard
- All communication is secured via HTTPS

## Validation Capability

The dashboard goes beyond simple detection by validating whether discovered issues are:

- Confirmed exploitable in the current environment
- Not exploitable in practice due to mitigating factors

## Challenges Faced & Ongoing Work

- **API Gateway Timeout Constraints**: The AWS API Gateway has a 29-second timeout limit, which means real-time scans cannot complete within this window for most AWS environments. Users currently need to navigate to the "Previous Scans" section to check completed scan results.
- **Authentication Implementation**: Implementing Cognito authentication required overcoming several challenges related to client secrets and authentication flows to ensure secure access while maintaining a seamless user experience.
- **Lambda Function Limitations**: The current Lambda functions have limited IAM roles to prevent timeout issues. This restricts the scope of what can be scanned in a single operation.

## Future Enhancements

- **Custom Scanning Profiles**: Allowing users to select specific types of scans to perform based on their security priorities and time constraints.
- **Compliance Reporting**: Adding predefined reports for common compliance frameworks such as CIS, NIST, and PCI DSS.
- **LangGraph Integration Optimization**: The current implementation uses LangGraph for intelligent analysis of AWS configurations. Optimizing this process is ongoing to improve performance and reduce execution time.
- **Amazon Bedrock Integration**: Exploring integration with Amazon Bedrock's foundation models to provide AI-powered security analysis, more detailed remediation steps, and advanced threat detection capabilities.