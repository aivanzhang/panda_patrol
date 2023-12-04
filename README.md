# <img src="panda-patrol.png" alt="Panda Patrol" width="50"/> Panda Patrol
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg) 

Gain greater visibility and context into your data pipelines with dashboards, alerting, silencing and other features built around your existing data tests and data profiling tools — within each step of your data pipelines. Add <ins> **less than 5 lines of code** </ins> and just run your pipelines as you normally would. Panda Patrol will take care of the rest.

**Questions and feedback** 

Email: ivanzhangofficial@gmail.com

Call: https://calendly.com/aivanzhang/chat

## Table of Contents
- [Integrations](#integrations)
- [Features](#features)
    - [AI-Generated Data Tests](#ai-generated-data-tests)
    - [General Data Tests](#general-data-tests)
    - [Anomaly Detection](#anomaly-detection)
    - [Data Test Results](#storing-data-test-results)
    - [Data Test Parameters](#data-test-parameters)
    - [Monitor Data Pipeline Steps](#monitor-data-pipeline-steps)
    - [Alerting](#alerting)
    - [Silencing](#silencing)
    - [Data Profiles](#data-profiles)
- [Demo](#demo)
- [Getting Started](#getting-started)

## Integrations
- [x] **Custom python data pipeline** <img src="python.svg" alt="python" width="16"/>
- [x] **Airflow** <img src="airflow.png" alt="airflow" width="16"/>
- [x] **Dagster** <img src="dagster.png" alt="dagster" width="16"/>
- [x] **Prefect** <img src="prefect.png" alt="prefect" width="16"/>
- [x] **dbt core (>=1.5)** <img src="dbt.png" alt="dbt-core" width="16"/>
- [ ] **dbt cloud** <img src="dbt.png" alt="dbt-cloud" width="16"/>

For examples of each integration, see [examples](examples).

## Features
This section describes the features of Panda Patrol at a high level. See [demo](#demo) for a short walkthrough of each feature. See [wiki](https://github.com/aivanzhang/panda_patrol/wiki) to learn how to implement each feature and more details.

### AI-Generated Data Tests
Don't know what data tests to write? No problem. Panda Patrol can generate data tests for you. Just pass in the headers, a preview of the data, and optional additional context.

### General Data Tests
Want to get started with a few quick, easy, general, and important data tests? Panda Patrol comes pre-built with a few data tests that run on your data. The best part? It only takes one function call to run these tests.

### Anomaly Detection
Want to quickly check for anomalies in a column? Panda Patrol can do that for you. Panda Patrol uses the ECOD anomaly detection model from the [pyod](https://github.com/yzhao062/pyod) open source anomaly detection library. Just pass in the excepted distribution of the column and the current distribution of the column. Panda Patrol detect and surface any anomalies. Even better, customize your own anomaly detection model and pass it in to Panda Patrol.

### Data Test Results
Write Python-based data tests right within your pipelines. Panda Patrol will store the results of each data test — the test code, logs, return value, start time, end time, exception (if any), and more — in a database. These results can be tracked in a general dashboard (with high level context like test status) and a dashboard for each pipeline run (with all the context w.r.t. the test).

### Data Test Parameters
Data changes all the time. Your data tests should change to accomodate these changes. With Panda Patrol, you can pass in parameters to your data tests and later change these parameters on the frontend — with just one function call.

### Monitor Data Pipeline Steps
Monitor each step of your pipeline so that you know each step is running as expected. Panda Patrol will store the start time, end time, and status of each step in a database. This gives you a high-level overview of your pipeline and allows you to drill down into each step to see more details.

### Alerting
Be notified when your data tests fail. Configure your own email and Slack settings to receive alerts. Alerts provide all the details you see in the dashboards so you get all the context you need to debug pipelines.

### Silencing
Want to skip and silence a data test? No problem. Silencing a data test is as easy as clicking a button and choosing a time.

### Data Profiles
Using a custom data profiling tool? Or an open-source tool like [ydata-profiling](https://github.com/ydataai/ydata-profiling)? Store data profiles (that are in JSON or HTML format) and check them to see what your data looks like at each step of your pipeline.

### Fully Self-Hosted
The best part? Panda Patrol can be fully self-hosted; this repository contains its backend and frontend code. You can run it on your own infrastructure and have full control over your data. No need to worry about data privacy and security.

## Demo
See demo here: https://www.loom.com/share/0468aef48b1843f381146399f1652b81?sid=107df0c0-3e53-4d3c-b9f2-1159d3f23bdf

## Getting Started
Check out the [Quickstart](https://github.com/aivanzhang/panda_patrol/wiki/Quickstart) guide to get started.

You can also look at examples of how Panda Patrol fits into your data pipeline. For example, if you use dagster, see [examples/dagster](examples/dagster) for a guide on how to get started with dagster. All guides should take no longer than **10 minutes** to complete. See [examples](examples) for all examples.

For documentation on how to use Panda Patrol and more details on each feature, see the [wiki](https://github.com/aivanzhang/panda_patrol/wiki).
