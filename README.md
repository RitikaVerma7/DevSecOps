# 🔐 CI/CD Automation & Security Testing – Online Restaurant Reservation System

### 👤 Contributor: Ritika Verma  
*ISBA 2408 – Software Project Management @ Santa Clara University*

---

## 🚀 Project Overview

This project focuses on enhancing restaurant reservation systems by integrating **DevOps practices**—particularly Continuous Integration and Continuous Deployment (CI/CD)—to automate delivery, improve system security, and scale reliably for small to mid-sized restaurants.

---

## 🛠️ My Role: CI/CD Automation & Security Champion

I was solely responsible for:

- **Setting up the entire CI/CD pipeline** from scratch using **GitLab**
- **Designing and implementing end-to-end automation workflows**
- **Writing security-focused test cases** to harden the system
- Embedding **security, quality, and performance** testing into every commit
- Ensuring only **thoroughly tested and verified code** was deployed to production

---

## ⚙️ CI/CD Pipeline – Built from the Ground Up

Implemented a **multi-stage GitLab pipeline** with the following:

- **Stages:** `lint` → `test` → `build` → `deploy`
- **Tools & Technologies:**
  - `GitLab CI/CD` for pipeline orchestration
  - `Docker` for containerization and deployment
  - `PyTest` for test automation
  - `HTMLHint` and `CSSLint` for frontend code quality

### 🔄 Automation Features:

- Complete automation of **build, test, and deploy** processes
- **Automated failure notifications** with GitLab artifacts
- Built-in support for **incremental delivery**, rollback, and traceability
- Reduced manual work and **eliminated human error risks**

---

## 🧪 Security-First Testing Strategy

I authored and implemented **comprehensive test cases** across all layers:

### 🔐 Security Tests:

- **SQL Injection Protection**  
  - Input sanitization for login fields (e.g., `"' OR '1'='1'--"`)
- **XSS Defense**
  - Validated against scripts like `<script>alert('XSS')</script>`
- **Input Validation**
  - Tested for excessively long strings and special characters
- **Authentication Flow**
  - Ensured secure session handling, error messaging, and no data leakage

### 🧩 Additional Testing Types:

- **Unit & Integration Testing:**  
  Validated login, order placement, and full user flows
- **Load Testing:**  
  Simulated concurrent requests to evaluate stability under pressure
- **Cross-Browser Compatibility:**  
  Ensured consistent behavior across Chrome, Safari, Firefox, and mobile devices

---

## 📄 Key Deliverables I Produced:

- Custom test scripts for PyTest and integration flow
- GitLab YAML config with artifact retention and conditional deploys
- QA logs: `qa_test_results.log`, `security_test_results.log`
- Linting reports: `lint_results.txt`
- Dockerized application containers for deployment

---

## ✅ Outcome & Impact

Thanks to the CI/CD setup and security testing I implemented:

- The team achieved **zero-downtime deployments**
- **Critical vulnerabilities were proactively identified and fixed**
- Developers received **instant feedback** on every push
- The system became **resilient, scalable, and secure by design**

---

## 📝 Final Thoughts

This project reflects my passion for combining **automation, security, and reliability** in real-world systems. By owning the entire CI/CD and security testing workflow, I ensured our restaurant reservation platform was not just functional—but **secure, maintainable, and production-ready**.

---
