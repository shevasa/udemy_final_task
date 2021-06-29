async def construct_info(state_data: dict):
    price = state_data.get('price')
    name = state_data.get('name')
    description = state_data.get('description')
    add_to_post = ["Пусто"]
    if name:
        add_to_post.append(f'Название: {name}')
    if description:
        add_to_post.append(f'Описание: {description}')
    if price:
        add_to_post.append(f'Цена: {price}')
    if len(add_to_post) > 1:
        return add_to_post[1:]
    else:
        return add_to_post[0]
