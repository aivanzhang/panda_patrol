# <img src="panda-patrol.png" alt="Panda Patrol" width="50"/> Panda Patrol
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg) 

Gain greater visibility and context into your data pipelines with dashboards, alerting, silencing and other features built around your existing data tests and data profiling tools — within each step of your data pipelines. Add <ins> **less than 5 lines of code** </ins> and just run your pipelines as you normally would. Panda Patrol will take care of the rest.

**Questions and feedback** 

Email: ivanzhangofficial@gmail.com

Call: https://calendly.com/aivanzhang/chat

## Table of Contents
- [Integrations](#integrations)
- [Features](#features)
    - [Data Test Results](#storing-data-test-results)
    - [Data Test Parameters](#data-test-parameters)
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

### Data Test Results
Write Python-based data tests right within your pipelines. Panda Patrol will store the results of each data test — the test code, logs, return value, start time, end time, exception (if any), and more — in a database. These results can be tracked in a general dashboard (with high level context like test status) and a dashboard for each pipeline run (with all the context w.r.t. the test).

### Data Test Parameters
Data changes all the time. Your data tests should change to accomodate these changes. With Panda Patrol, you can pass in parameters to your data tests and later change these parameters on the frontend — with just one function call.

### Alerting
Be notified when your data tests fail. Configure your own email and Slack settings to receive alerts. Alerts provide all the details you see in the dashboards so you get all the context you need to debug pipelines.

### Silencing
Want to skip and silence a data test? No problem. Silencing a data test is as easy as clicking a button and choosing a time.

### Data Profiles
Using a custom data profiling tool? Or an open-source tool like [ydata-profiling](https://github.com/ydataai/ydata-profiling)? Use Panda Patrol to store data profiles (that are in JSON or HTML format). Check these profiles to see what your data looks like at each step of your pipeline.

### Fully Self-Hosted
The best part? Panda Patrol is fully self-hosted; this repository contains its backend and frontend code in its entirety. You can run it on your own infrastructure and have full control over your data. No need to worry about data privacy and security.

## Demo
See demo here: https://www.loom.com/share/864441c4e8034ea2adaf340ca69d988b?sid=7dc6f10a-b0f6-4a5c-927c-09e14289c6ca

## Getting Started
Check out the [Quickstart](https://github.com/aivanzhang/panda_patrol/wiki/Quickstart) guide to get started.

You can also look at examples of how Panda Patrol fits into your data pipeline. For example, if you use dagster, see [examples/dagster](examples/dagster) for a guide on how to get started with dagster. All guides should take no longer than **10 minutes** to complete. See [examples](examples) for all examples.

For documentation on how to use Panda Patrol and more details on each feature, see the [wiki](https://github.com/aivanzhang/panda_patrol/wiki).
