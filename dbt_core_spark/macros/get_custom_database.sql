{% macro generate_database_name(custom_database_name=none, node=none) -%}

    {%- set default_database = target.database -%}

    {%- if target.name != 'prod' -%}

        {%- if custom_database_name is none -%}

            {{ default_database }}

        {%- else -%}

            {{ default_database }}_{{ custom_database_name | trim }}

        {%- endif -%}

    {%- else -%}

        {%- if custom_database_name is none -%}

            {{ default_database }}

        {%- else -%}

            {{ custom_database_name | trim }}

        {%- endif -%}

    {%- endif -%}

{%- endmacro %}