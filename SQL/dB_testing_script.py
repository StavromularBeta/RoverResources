from SQL.dB_add_delete import AddDelete
from SQL.dB_select import Select
import datetime

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

# can join one or two tables together (left join).
 

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

new_selection.
    left_join_two_tables("categories.category_name, products.name",
                         "products",
                         "products.categories_id",
                         "categories",
                         "categories.id",
                         "categories.category_name",
                         True)
                         
# adding new credentials, and a new user

new_entry.new_credentials_record("Full")
new_entry.new_user_record((1, "Peter", "12345"))
new_entry.new_requests_record((3, 1, datetime.date.today(), 4))
new_selection.select_all_from_table("requests", True)

# selecting the requests for a user

new_selection.
    left_join_three_tables("p.name, p.product_code, r.request_date, r.amount, u.user_name",
                           "requests r",
                           "r.products_id",
                           "products p",
                           "p.id",
                           "r.users_id",
                           "users u",
                           "u.id",
                           "u.user_name",
                           True)

# selecting the requests for a user with vendor information



new_selection.\
    left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date, r.amount," +
                              "u.user_name",
                              [["requests r", "", "r.products_id"],
                               ["products p", "p.id", "r.users_id"],
                               ["users u", "u.id", "p.vendors_id"],
                               ["vendors v", "v.id", "p.categories_id"],
                               ["categories c", "c.id", ""]],
                              "u.user_name",
                              True)

new_selection.select_all_from_table("users", True)

"""

new_entry.new_credentials_record(("Full", "Grants Full Access to all functionality."))
new_entry.new_credentials_record(("Basic", "Grants the lowest level of functionality."))

new_entry.new_user_record((2, "Peter", "12345", "Programmer"))
new_entry.new_user_record((2, "Rachel", "12345", "Made Up Person"))
new_entry.new_user_record((1, "Wendy", "12345", "Manager"))

new_entry.new_categories_record(("standards", "analytical standards for QC of methods."))
new_entry.new_categories_record(("media", "media for culturing bacteria."))
new_entry.new_categories_record(("office supplies", "standard office supplies."))
new_entry.new_categories_record(("general equipment", "things like desks, chairs, etc."))
new_entry.new_categories_record(("chemicals", "Chemicals for use in analytical methods."))
new_entry.new_categories_record(("labware", "Equipment used in analytical methods."))
new_entry.new_categories_record(("other", "Objects that don't fit an existing category."))

new_entry.new_sub_categories_record((1, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((1, "Cannabinoids", "Standards for use in Cannabis Potency."))
new_entry.new_sub_categories_record((1, "Cultures", "Cultures to be used as standards."))
new_entry.new_sub_categories_record((1, "Biotoxins", "Standards for use in Biotoxins methods.."))
new_entry.new_sub_categories_record((1, "Pesticides", "Standards for use in Health Canada Pesticides."))
new_entry.new_sub_categories_record((1, "Terpenes", "Terpenoids for use in Terpene analysis.."))
new_entry.new_sub_categories_record((1, "Organic Chem", "Misc. Organic Chemistry Standards."))
new_entry.new_sub_categories_record((1, "Inorganic Chem", "Misc. Inorganic Chemistry Standards."))
new_entry.new_sub_categories_record((2, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((3, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((4, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((5, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((6, "None", "No subcategory applies."))
new_entry.new_sub_categories_record((7, "None", "No subcategory applies."))

new_entry.new_vendors_record(("Sigma-Aldrich", "Supplier of standards and other chemicals."))
new_entry.new_vendors_record(("Restek", "Supplier of standards."))
new_entry.new_vendors_record(("Oxoid", "Supplier of Media."))
new_entry.new_vendors_record(("Dell", "Supplier of Computers."))
new_entry.new_vendors_record(("Phenomenex", "Supplier of Analytical Columns."))

"""
new_entry.new_products_record((1, 7, 1, "I4883", "Ibuprofen (>98%)", "Internal Standard for Cannabis Potency."))
new_entry.new_products_record((1, 2, 1, "C-144", "Cannabidiolic acid solution", "CBDA for Cannabis Potency."))
new_entry.new_products_record((1, 2, 1, "34090", "d8-Tetrahydrocannabinol (d8-THC) Standard",
                               "d8-THC for Cannabis Potency."))


new_entry.new_products_record((5, 12, 1, "320331", "Hydrochloric acid", "Hydrochloric Acid for Metals analysis."))
"""