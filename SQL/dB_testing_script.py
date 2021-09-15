from SQL.dB_add_delete import AddDelete
from SQL.dB_select import Select

new_entry = AddDelete()
new_selection = Select()

"""
Adding Wendy's Categories to the categories table.

new_entry.new_categories_record("standards")
new_entry.new_categories_record("media")
new_entry.new_categories_record("office supplies")
new_entry.new_categories_record("general equipment")
new_entry.new_categories_record("chemicals")
new_entry.new_categories_record("labware")
new_entry.new_categories_record("other")
"""

new_selection.select_all_from_table("categories", True)
new_selection.select_all_from_table_where_one_field_like("categories", "category_name", "%stan%", True)
new_selection.select_all_from_table_where_one_field_equals("categories", "category_name", "standards", True)
