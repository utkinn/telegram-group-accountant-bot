from accountant.model.collection import Collection, Spend


def test_without_spend():
    # Create a sample collection
    collection = Collection(
        spends=[
            Spend(name="A", amount=10, spender_user_name="foo"),
            Spend(name="B", amount=20, spender_user_name="bar"),
            Spend(name="C", amount=30, spender_user_name="baz"),
        ]
    )

    # Test removing the first spend
    result = collection.without_spend(0)
    assert len(result.spends) == 2
    assert result.spends[0].amount == 20
    assert result.spends[1].amount == 30

    # Test removing the middle spend
    result = collection.without_spend(1)
    assert len(result.spends) == 2
    assert result.spends[0].amount == 10
    assert result.spends[1].amount == 30

    # Test removing the last spend
    result = collection.without_spend(2)
    assert len(result.spends) == 2
    assert result.spends[0].amount == 10
    assert result.spends[1].amount == 20

    # Test removing a spend from an empty collection
    empty_collection = Collection(spends=[])
    result = empty_collection.without_spend(0)
    assert len(result.spends) == 0
