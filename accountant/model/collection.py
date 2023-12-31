from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Spend:
    name: str
    amount: int
    spender_user_name: str


@dataclass(frozen=True)
class Invoice:
    payee_user_name: str
    amount: int


@dataclass(frozen=True)
class Collection:
    name: str = field(default_factory=lambda: datetime.now().strftime("%d.%m.%Y"))
    created_at: datetime = field(default_factory=datetime.now)
    spends: list = field(default_factory=list)

    def with_new_spend(self, spend: Spend) -> "Collection":
        return replace(self, spends=[*self.spends, spend])
    
    def without_spend(self, spend_num: int) -> "Collection":
        return replace(self, spends=[*self.spends[:spend_num], *self.spends[spend_num + 1:]])

    def spread(self, payers_count: int) -> list[Invoice]:
        spending_sums_per_payer = {spend.spender_user_name: 0 for spend in self.spends}
        for spend in self.spends:
            spending_sums_per_payer[spend.spender_user_name] += spend.amount
        return [
            Invoice(
                payee_user_name, spending_sums_per_payer[payee_user_name] / payers_count
            )
            for payee_user_name in spending_sums_per_payer
        ]
    
    def renamed(self, new_name: str) -> "Collection":
        return replace(self, name=new_name)
