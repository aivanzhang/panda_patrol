from panda_patrol.patrols import patrol_group


def model(dbt, session):
    users_df = dbt.ref("users_view")
    orders_df = dbt.ref("orders_view")
    products_df = dbt.ref("products_view")

    # Join users and orders on user_id
    user_orders_df = users_df.merge(orders_df, on="user_id", how="inner")

    # Join the result with products on product_name
    final_df = user_orders_df.merge(products_df, on="product_name", how="inner")

    with patrol_group("User Orders") as patrol:

        @patrol("All prices are positive")
        def prices_are_positive(patrol_id):
            assert (final_df["price"] > 0).all()
            print("All prices are positive")

    return final_df
