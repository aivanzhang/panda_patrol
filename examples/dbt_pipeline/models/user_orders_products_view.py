from ydata_profiling import ProfileReport
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter
from panda_patrol.profilers import save_report


def model(dbt, session):
    users_df = dbt.ref("users_view")
    orders_df = dbt.ref("orders_view")
    products_df = dbt.ref("products_view")

    # Join users and orders on user_id
    user_orders_df = users_df.merge(orders_df, on="user_id", how="inner")

    # Join the result with products on product_name
    final_df = user_orders_df.merge(products_df, on="product_name", how="inner")

    with patrol_group("User Orders", "user_orders_products_view") as patrol:

        @patrol("All prices within expected range")
        def prices_within_range(patrol_id):
            print(final_df)
            min_price = float(adjustable_parameter("min_price", patrol_id, 0))
            max_price = float(adjustable_parameter("max_price", patrol_id, 100000))
            assert (
                final_df["product_price"] >= min_price
            ).all(), f"Found value less than the min of {min_price}"
            assert (
                final_df["product_price"] <= max_price
            ).all(), f"Found value more than the max of {max_price}"
            return final_df.describe().to_dict()

    report = ProfileReport(final_df)
    save_report(report.to_html(), "User Orders", "User Orders Profiling Report", "html")

    return final_df
