resource "snowflake_warehouse" "reddit_xs" {
  name           = "reddit_xs"
  comment        = "Small warehouse for debugging."
  warehouse_size = "xsmall"
}

resource "snowflake_warehouse_grant" "reddit_xs" {
  warehouse_name = snowflake_warehouse.reddit_xs.name
  privilege      = "USAGE"

  roles = [
    snowflake_role.streamlit.name,
    snowflake_role.confluent.name,
    data.snowflake_role.accountadmin.name
  ]
}
