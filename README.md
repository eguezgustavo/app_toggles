# App toggles library

![CI](https://github.com/eguezgustavo/app_toggles/actions/workflows/ci.yaml/badge.svg?branch=main)

This library has been created taking into account the work done by [Pete Hodgson](https://thepete.net/) published in [https://martinfowler.com/](https://martinfowler.com/articles/feature-toggles.html).

## How to use it
The example below uses a sample feature to include a cancellation link in a email so the user can cancel the sales order.

1. Create the /tmp/test_app_toggles.json file with the following content:
``` json
{
    "isOrderCancellationEnabled": true,
    "isAutoRefundEnable": false
}
```
2. Run the app

``` python
import app_toggles

provider = app_toggles.JsonToggleProvider("/tmp/test_app_toggles.json")
toggles = app_toggles.Toggles(provider=provider)


@toggles.toggle_decision
def usage_of_order_cancellation_email(get_toggles, when_on, when_off):
    order_cancellation_enabled, auto_refund_enabled = get_toggles(
        ["isOrderCancellationEnabled", "isAutoRefundEnable"]
    )
    if order_cancellation_enabled and auto_refund_enabled:
        return when_on
    return when_off


def create_email_body(client_name: str, sales_order_number: str) -> str:
    header = f"""
    Dear {client_name},

    Your order number {sales_order_number} has bee approved.
    """

    footer = """
    Cheers,

    Your company team
    """

    cancellation_text = usage_of_order_cancellation_email(
        when_on=f"To cancel your order follow this link: http://cancel/{sales_order_number}",
        when_off="",
    )

    return f"""
    {header}
    {cancellation_text}
    {footer}
    """

body = create_email_body("Gustavo", "2342937")
print(body)
```

3. Feel free to change the value of the toggles in the JSON file and see how the email body changes

## How to extend this library
The library exposes a "Provider" interface. You can create your own interface to interact with external services that manage feature flags. Below you' ll find a sample code used to retrieve toggles stored in memory.

DON'T FORGET TO CREATE A PR SO WE CAN ADD THE IMPLEMENTATION YOU'VE CREATED!

```python
import typing

import app_toggles


class InMemoryProvider(app_toggles.Provider):
    toggles = {
        "isOrderCancellationEnabled": True,
        "isAutoRefundEnable": True
    }

    def get_toggles(self, toggle_names: typing.List[str]) -> typing.Tuple[bool]:
        missing_toogles = [toggle for toggle in toggle_names if toggle not in InMemoryProvider.toggles]

        if missing_toogles:
            raise app_toggles.ToggleNotFoundError(f"The follwing toggles where not found: {', '.join(missing_toogles)}")

        return [
            toggle_value
            for toggle_name, toggle_value in InMemoryProvider.toggles.items()
            if toggle_name in toggle_names
        ]

```
