# 📌 CI/CD Integration and Testing – DevSecOps

### 👤 Contributor: Ritika Verma  
*Part of ISBA 2408 – Software Project Management @ Santa Clara University*

---

## 🚀 Project Overview

This project aims to modernize restaurant reservation systems by developing a cloud-based web platform integrated with a CI/CD pipeline. The system is designed to automate software delivery, enhance testing, ensure zero-downtime deployment, and improve scalability and security for small to medium-sized restaurants.

---

## 🔧 My Role: CI/CD Pipeline & Testing

I was responsible for designing and implementing the **GitLab-based CI/CD pipeline** and creating a **robust testing strategy** to ensure continuous quality and secure deployment of the system.

---

## ⚙️ CI/CD Pipeline Setup (GitLab)

- **Pipeline Stages:** `lint` → `test` → `build` → `deploy`
- **Tools Used:**  
  - `PyTest` for backend unit/integration/security testing  
  - `HTMLHint` and `CSSLint` for frontend linting  
  - `Docker` for packaging and deployment  
- **Key Features:**
  - Automated test execution on each commit
  - Logging and archiving test results via GitLab artifacts
  - Conditional deployment only if all tests pass
  - Resilient configuration using `allow_failure` and `only` conditions

---

## 🧪 Testing Strategy

Testing was a central part of my contribution, embedded within the CI/CD workflow.

### 🔹 Testing Types:
- **Unit Testing** – Core modules like login and order processing
- **Integration Testing** – End-to-end user flows (e.g., login → place order)
- **Security Testing** – Simulated attacks like SQL Injection and XSS
- **Performance Testing** – Load handling during peak order times
- **Compatibility Testing** – Multi-browser and device support

### 🔹 Highlights of Test Cases:
- **TC_LOGIN_01**: Valid login flow  
- **TC_INT_ORDER_02**: Input validation on empty order
- **TC_SEC_01**: SQL injection rejection
- **TC_PERF_01**: High-concurrency stress testing

### 🔹 GitLab Artifacts Generated:
- `qa_test_results.log`  
- `security_test_results.log`  
- `lint_results.txt`

---

## 📈 Impact of My Work

- Ensured secure, bug-free, and high-performance deployments
- Enabled continuous feedback for developers via automated reports
- Reduced production errors through early defect detection
- Maintained compliance and traceability through standardized logs

---

## 📝 Final Notes

My contribution emphasized the **real-world power of automation in DevOps**. By integrating continuous testing and deployment practices, I helped build a system that evolves rapidly, securely, and with minimal downtime—helping restaurant operations stay focused on customer satisfaction.
