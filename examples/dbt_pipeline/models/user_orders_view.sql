SELECT
    u.user_id,
    u.username,
    o.order_id,
    o.product_name,
    o.order_date
FROM public.users u
JOIN public.orders o ON u.user_id = o.user_id
