"""Offline infrastructure budget estimates from explicit user-supplied rates."""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import sys


def number(value, field):
    if isinstance(value, bool):
        raise ValueError(field+' must be numeric')
    try:
        result=Decimal(str(value))
    except InvalidOperation:
        raise ValueError(field+' must be numeric') from None
    if not result.is_finite() or result < 0:
        raise ValueError(field+' must be finite and nonnegative')
    return result


def money(value):
    return str(value.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))


def estimate(config):
    hours=number(config.get('hours_per_month',730),'hours_per_month')
    if hours > 744: raise ValueError('hours_per_month cannot exceed 744')
    budget=number(config['monthly_budget'],'monthly_budget')
    headroom=number(config.get('headroom_percent',0),'headroom_percent')
    if headroom > 100: raise ValueError('headroom_percent cannot exceed 100')
    lines=[];total=Decimal(0);names=set()
    for service in config['services']:
        name=service['name']
        if not isinstance(name,str) or not name.strip() or name in names:
            raise ValueError('service names must be unique nonempty strings')
        names.add(name)
        quantity=number(service['quantity'],'quantity')
        rate=number(service['unit_price'],'unit_price')
        unit=service['unit']
        if unit not in ('hour','month'): raise ValueError('unit must be hour or month')
        cost=quantity*rate*(hours if unit=='hour' else 1)
        total+=cost
        lines.append({'name':name,'monthly_cost':money(cost)})
    reserve=total*headroom/100
    projected=total+reserve
    return {'currency':config.get('currency','USD'),'line_items':lines,
            'subtotal':money(total),'headroom':money(reserve),'projected_total':money(projected),
            'monthly_budget':money(budget),'remaining_budget':money(budget-projected),
            'over_budget':projected > budget}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario')
    args=parser.parse_args()
    try:
        output=estimate(json.loads(Path(args.scenario).read_text()))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'error':str(error)}),file=sys.stderr);return 2
    print(json.dumps(output,indent=2))
    return 1 if output['over_budget'] else 0

if __name__=='__main__': sys.exit(main())
