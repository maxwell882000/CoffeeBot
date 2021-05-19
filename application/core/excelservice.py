import xlrd
from . import dishservice
from application.core.models import DishCategory


def parse_excel_file(path_to_file: str):
    workbook = xlrd.open_workbook(path_to_file)
    worksheet = workbook.sheet_by_index(0)
    for rx in range(worksheet.nrows):
        if rx == 0:
            continue
        row = worksheet.row(rx)
        category_1 = row[1].value
        product_name = row[2].value
        parent_category = row[7].value
        category_2 = row[8].value
        category_3 = row[10].value
        description = row[11].value
        price = row[13].value
        image = row[14].value
        _create_product(product_name, parent_category, category_1, category_2, category_3, description, price, image)


def _create_category(category3_name, category2_name, category1_name, parent_category_name) -> DishCategory:
    parent_category = dishservice.get_category_by_name(parent_category_name, 'ru')
    if not parent_category:
        parent_category = dishservice.create_category(parent_category_name, parent_category_name)
    category1 = _get_or_create_category(category1_name, parent_category)
    category2 = _get_or_create_category(category2_name, category1)
    category3 = _get_or_create_category(category3_name, category2)
    if category3:
        return category3
    elif category2:
        return category2
    elif category1:
        return category1
    else:
        return parent_category


def _get_or_create_category(category_name, parent_category):
    if not category_name:
        return None
    category = dishservice.get_category_by_name(category_name, 'ru')
    if not category:
        category = dishservice.create_category(category_name, category_name, parent_category.id)
    return category


def _create_product(product_name, parent_category,
                    category1, category2, category3, product_description, product_price, image):
    if product_price:
        product_price = float(product_price)
    else:
        product_price = 0.0
    if category2 == 'Муфта':
        print()
        pass
    category = _create_category(category3, category2, category1, parent_category)
    dishservice.create_dish(product_name, product_name, product_description, product_description, str(image), product_price, category.id)
