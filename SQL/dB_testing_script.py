from SQL.dB_add_delete import AddDelete
from SQL.dB_select import Select

new_entry = AddDelete()
new_selection = Select()

"""

# Adding Wendy's Categories to the categories table.

new_entry.new_categories_record("standards")
new_entry.new_categories_record("media")
new_entry.new_categories_record("office supplies")
new_entry.new_categories_record("general equipment")
new_entry.new_categories_record("chemicals")
new_entry.new_categories_record("labware")
new_entry.new_categories_record("other")

# selecting all from a table. using select like to do a partial match (regex), using equals to do an exact match.

new_selection.select_all_from_table("categories", True)
new_selection.select_all_from_table_where_one_field_like("categories", "category_name", "%stan%", True)
new_selection.select_all_from_table_where_one_field_equals("categories", "category_name", "standards", True)

# adding some sample vendors to the vendors table.

new_entry.new_vendors_record("Sigma-Aldrich")
new_entry.new_vendors_record("Restek")
new_entry.new_vendors_record("VWR")
new_entry.new_vendors_record("Dell")
new_selection.select_all_from_table("vendors", True)

new_entry.new_products_record((1, 2, "RSTK567", "CBDA Standard (example)"))
new_entry.new_products_record((1, 1, "FGK-52", "Fluffygumkernol"))
new_entry.new_products_record((2, 2, "PEP2345", "Peptone mix (example)"))
new_entry.new_products_record((3, 4, "QRDGETXH", "Dell Workstation Computer"))

new_selection.select_all_from_table("products", True)

# union statement that joins two tables together. 

new_selection.left_join_table_one_table_two("categories.category_name",
                                            "products.*",
                                            "categories.id",
                                            "products.categories_id",
                                            "categories.id",
                                            True)

new_selection.left_join_table_one_table_two("vendors.vendor_name",
                                            "products.*",
                                            "vendors.id",
                                            "products.vendors_id",
                                            "vendors.id",
                                            True)

# lists the category, vendor, product code and product name for each item in the products table. 

new_selection.
    left_join_three_tables("categories.category_name, vendors.vendor_name, products.product_code, products.name",
                           "products",
                           "products.vendors_id",
                           "vendors",
                           "vendors.id",
                           "products.categories_id",
                           "categories",
                           "categories.id",
                           "categories.category_name",
                           True)

"""

