<p align="center">
  <a href="https://github.com/datarootsio/snowflake-ml"><img alt="logo" src="https://raw.githubusercontent.com/datarootsio/snowflake-ml/main/dashboard/static/logo.png"></a>
</p>
<p align="center">
  <a href="https://dataroots.io"><img alt="Maintained by dataroots" src="https://dataroots.io/maintained-rnd.svg" /></a>
  <a href="https://www.terraform.io/"><img alt="test" src="https://img.shields.io/badge/terraform-1.0.0-blueviolet" /></a>
  <img alt="Python versions" src="https://img.shields.io/badge/python-3.8-blue" />
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>
  <a href="https://github.com/datarootsio/snowflake-ml/actions"><img alt="test" src="https://github.com/datarootsio/snowflake-ml/actions/workflows/deploy_ml.yaml/badge.svg" /></a>
</p>

# Snowflake-ML

> Toy use case on using Snowflake as a full end-to-end ML platform.

## What's inside

- Terraform-managed infrastructure
  - [Snowflake](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest)
  - [Confluent Cloud](https://registry.terraform.io/providers/confluentinc/confluent/latest/docs)
- Snowflake
  - Python integration via [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html)
    - [UDFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python.html)
    - [Stored Procedures](https://docs.snowflake.com/en/sql-reference/stored-procedures-python.html)
  - [Tasks](https://docs.snowflake.com/en/user-guide/tasks-intro.html)
  - [Streams](https://docs.snowflake.com/en/user-guide/streams-intro.html)
  - [Materialized Views](https://docs.snowflake.com/en/user-guide/views-materialized.html)
- [Streamlit](https://streamlit.io/) dashboard application
- CI/CD via [GitHub Actions](https://github.com/features/actions)
  - Display model metrics via [CML](https://cml.dev/)
  - Update Snowflake UDFs
  - Tag versions

## Getting started

To get started, whether you want to contribute or run any applications, first clone the
repo and install the dependencies.

```console
git clone git@github.com:datarootsio/snowflake-ml.git
cd snowflake-ml
pip install poetry==1.1.2  # optional, install poetry if needed
poetry install
pre-commit install  # optional, though recommended - install pre-commit hooks
```

### Running app

```console
poetry run streamlit run dashboard/👋_hello.py
```

## How it works

The app is consists of

- Local Apache Kafka connector
- Apache Kafka cluster on Confluent Cloud
- Snowflake data warehouse
- Streamlit app (ran locally)

Where both Confluent Cloud and Snowflake infrastructure are managed by Terraform.

<img alt="ML Solution Architecture" src="https://raw.githubusercontent.com/datarootsio/snowflake-ml/main/dashboard/static/architecture.png">

Taking a closer look in Snowflake, we have the landing tables that are updated in real
time via Confluent Cloud's Snowflake Connector and
[Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro.html). From
there the data is transformed via views and
[materialized views](https://docs.snowflake.com/en/user-guide/views-materialized.html)
to get aggregate statistics. Alternatively we use Snowflake's
[streams](https://docs.snowflake.com/en/user-guide/streams-intro.html),
[tasks](https://docs.snowflake.com/en/user-guide/tasks-intro.html) and python
[UDFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python.html) to
transform the data using machine learning and store the predictions on a table that is
ingested by Streamlit.

<img alt="ML Solution Architecture" src="https://raw.githubusercontent.com/datarootsio/snowflake-ml/main/dashboard/static/architecture_snowflake.png">

## Support

This project is maintained by dataroots.For any questions, contact us at
murilo@dataroots.io 🚀
