# Software Requirements Specification (SRS)
**Project Title:** College Campus Lost & Found System
**Standard:** IEEE-830 Format

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the software requirements for the "College Campus Lost & Found System". It specifies the functional and non-functional requirements, and architectural design strategies for the final system deployment.

### 1.2 Scope
The web portal aims to centralize the reporting of lost and found items securely across a college campus. It utilizes a MySQL relational database managed dynamically by a Python Flask architecture. The portal features role-based access controls explicitly distinguishing `Student` clients and organizational `Admin` moderators.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification
- **ERD:** Entity Relationship Diagram
- **DFD:** Data Flow Diagram
- **SQL:** Structured Query Language
- **ORM:** Object Relational Mapper

## 2. Overall Description

### 2.1 Product Perspective
The system functions as a modular standalone web framework accessible over HTTP/HTTPS natively on smart devices and laptops minimizing friction via responsive web layout optimizations.

### 2.2 User Classes and Characteristics
1.  **Students (End Users):** Capable of signing up, authenticating, posting localized claims, isolating attributes (categories), and dictating item statuses (Lost vs Found vs Claimed).
2.  **Administrator (Management):** A superuser controlling a private dashboard that manipulates metrics, globally purges inappropriate content natively, and forcefully disables erratic accounts.

### 2.3 Operating Environment
-   **Client Side:** Modern Web-Browser execution (Chrome, Safari, Firefox, Edge).
-   **Server System:** Application Layer parsed over Python 3.x, Database mounted over MySQL Server 8+.

---

## 3. Diagrams & Project Management Planning

### 3.1 Gantt Chart
Visualizing task progression scheduling standardizing a 2-week implementation lifecycle.

```mermaid
gantt
    title Lost & Found Project Schedule
    dateFormat  YYYY-MM-DD
    section Phase 1: Planning
    Requirement Gathering    :a1, 2026-04-01, 2d
    System Design (UML/DB)   :a2, after a1, 3d
    section Phase 2: Execution
    Database Architecture    :a3, after a2, 2d
    Backend Core (Flask)     :a4, after a3, 4d
    Frontend UI Integration  :a5, after a3, 4d
    section Phase 3: QA
    Unit Testing & Debug     :a6, after a5, 2d
    User Acceptance & Deploy :a7, after a6, 2d
```

### 3.2 PERT Chart
Illustrating strict milestone task dependencies natively.

```mermaid
graph TD
    A[Start Planning] --> B[Requirement Analysis]
    B --> C[UML & DB Arch]
    C --> D[MySQL Setup]
    C --> E[Interface Mockups]
    D --> F[Flask Backend Dev]
    E --> G[Frontend Templates]
    F --> H[Integration Checkpoint]
    G --> H
    H --> I[Vulnerability Testing]
    I --> J[Production Rollout]
```

### 3.3 Use Case Diagram
Mapping actor access functionality.

```mermaid
flowchart LR
    subgraph System Platform
        UC1(Account Registration)
        UC2(Create/Edit Items)
        UC3(Global Filter/Search)
        UC4(Delete Flagged Users)
        UC5(Delete Any System Item)
        UC6(View Statistics)
    end
    
    Student((Student Role))
    Admin((Admin Role))
    
    Student --> UC1
    Student --> UC2
    Student --> UC3
    
    Admin --> UC1
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
```

### 3.4 Activity Diagram
Flowing state conditional logic for standard user workflow.

```mermaid
stateDiagram-v2
    [*] --> AuthGate
    AuthGate --> LoginSuccess : Valid Credentials
    AuthGate --> AuthGate : Invalid Email/Pass
    
    LoginSuccess --> MainDashboard
    
    MainDashboard --> PostItem : Trigger Addition
    PostItem --> Validation : Check Data & Images
    Validation --> DatabaseWrite : Safe Data
    Validation --> PostItem : Reject Errors
    DatabaseWrite --> MainDashboard
    
    MainDashboard --> SearchFilter
    SearchFilter --> ItemDetail
    ItemDetail --> StatusMutation : Verify Origin Owner
    StatusMutation --> DatabaseWrite
    
    MainDashboard --> [*] : Terminate/Logout
```

### 3.5 Sequence Flow Diagram
Interaction between view layer, backend controller, and SQL schema mappings.

```mermaid
sequenceDiagram
    actor StandardUser
    participant UI as Frontend Interface
    participant Py as Flask Dispatcher
    participant SQL as MySQL Gateway
    
    StandardUser->>UI: Select "Add Item"
    UI->>Py: POST /item/add (+Image)
    Py->>Py: OS Check Secure Filename
    Py->>Py: Authenticate Session ID
    Py->>SQL: INSERT INTO item (title, desc...)
    SQL-->>Py: Commit Complete Execution
    Py-->>UI: Returning HTTP 302 / Flash Success
    UI-->>StandardUser: Redirect to Feed View
```

---

## 4. DFD (Data Flow Diagrams)

### 4.1 Level 0 (Context Level Diagram)
```mermaid
flowchart LR
    S[Student Actor] -- User Action / Data --> LFS((Central Lost\n& Found System))
    LFS -- Status Updates / Result Pages --> S
    A[Global Admin] -- Moderate Queries --> LFS
    LFS -- Analytics Metrics --> A
```

### 4.2 Level 1 Diagram
```mermaid
flowchart TD
    U[App Client] -->|Login Token| P1((1.0 Setup Auth Session))
    P1 -->|Query| DB1[(User Database)]
    DB1 -->|Valid Result| P1
    
    U -->|Action Data| P2((2.0 Handle Post Creation))
    P2 -->|Save Action| DB2[(Item File/DB records)]
    
    U -->|Search Syntax| P3((3.0 Execution Search Queue))
    DB2 -->|Return Sets| P3
    P3 -->|Render DOM| U
    
    Admin[Admin Client] -->|Action Commands| P4((4.0 Admin Actions))
    P4 -->|Enforce Deletions| DB1
    P4 -->|Enforce Purge| DB2
```

### 4.3 Level 2 Diagram (Exploding 2.0 Item Management)
```mermaid
flowchart TD
    In[Client Submission] --> P21((2.1 Form Sanitation validation))
    P21 --> |Invalid| Reg((Reject Submission))
    P21 --> |Valid Data| P22((2.2 Secure Media Image Processor))
    P22 --> |Write File| FS[(Static /uploads FS)]
    P22 --> P23((2.3 ORM Model Construction))
    P23 --> |SQL Parameterization| DB[(MySQL items table)]
    DB --> Out[Confirmation Output Dispatcher]
```

---

## 5. Database Specification

### 5.1 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ ITEM : "Uploads/Owns"
    USER {
        int id PK
        varchar(150) name
        varchar(150) email
        varchar(256) password_hash
        varchar(20) role "student | admin"
    }
    ITEM {
        int id PK
        varchar(150) title
        text description
        varchar(50) category "Electronics, Books..."
        varchar(50) status "Lost, Found, Claimed"
        varchar(255) image_path
        datetime date_reported
        varchar(150) location
        varchar(150) contact_info
        int user_id FK
    }
```

### 5.2 Database Structure in Table Form

**`user` Table**

| Field | Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| **id** | Integer | **PRIMARY KEY**, Auto Increment | Unique record identifier per user. |
| **name** | Varchar(150) | NOT NULL | User's full legal name. |
| **email** | Varchar(150) | NOT NULL, UNIQUE | Campus email used for authorization logic. |
| **password_hash** | Varchar(256) | NOT NULL | Werkzeug securely encrypted string. |
| **role** | Varchar(20) | NOT NULL, default='student' | Determines access permission elevation. |

**`item` Table**

| Field | Type | Attributes | Description |
| :--- | :--- | :--- | :--- |
| **id** | Integer | **PRIMARY KEY**, Auto Increment | Master identification for platform objects. |
| **title** | Varchar(150) | NOT NULL | Short descriptor / Header. |
| **description** | Text         | NOT NULL | Elaborated visual descriptors/warnings. |
| **category** | Varchar(50)  | NOT NULL | Group selector (Accessory, Laptop etc.) |
| **status** | Varchar(50)  | NOT NULL | State tracking indicator. |
| **image_path** | Varchar(255) | NULLABLE | Relative static file directory mapper link. |
| **date_reported**| DateTime     | NOT NULL, default=NOW() | Automatically logs upload timing. |
| **location** | Varchar(150) | NOT NULL | Where physically it was lost/discovered. |
| **contact_info** | Varchar(150) | NOT NULL | Phone or instructions to meet/verify identity. |
| **user_id** | Integer      | **FOREIGN KEY** (user.id) | Author tracing relationship schema. |

---
**End of IEEE 830 Specification Documents.**
