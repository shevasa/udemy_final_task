from aiogram import types

STANDART_SHIPPING = types.ShippingOption(
    id="1",
    title='FCA',
    prices=[
        types.LabeledPrice(label='Транспорт',
                           amount=1000 * 100),
        types.LabeledPrice(label='Картонная упаковка',
                           amount=50 * 100)
    ]
)

MINIMAL_SHIPPING = types.ShippingOption(
    id="2",
    title='EXW',
    prices=[
        types.LabeledPrice(label='Картонная упаковка',
                           amount=50 * 100)
    ]
)

MAXIMUM_SHIPPING = types.ShippingOption(
    id="3",
    title='DAF',
    prices=[
        types.LabeledPrice(label='Наземный транспорт',
                           amount=1000 * 100),
        types.LabeledPrice(label='Картонная упаковка',
                           amount=50 * 100),
        types.LabeledPrice(label='Морской транспорт',
                           amount=3000 * 100)
    ]
)
