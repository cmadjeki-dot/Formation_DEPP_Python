import pandas as pd

from src.data.simulate_depp import generate_student_dataset, inject_quality_issues


def test_generate_student_dataset_has_expected_columns():
    data = generate_student_dataset(n_students=1500)
    expected = {
        "id_eleve",
        "sexe",
        "pcs",
        "retard",
        "academie",
        "type_etab",
        "ressources_num",
        "age",
        "score_lecture",
    }
    assert set(data.columns) == expected
    assert len(data) == 1500
    assert data["score_lecture"].between(0, 100).all()


def test_inject_quality_issues_keeps_dataframe_shape_and_nan():
    data = generate_student_dataset(n_students=200)
    enriched = inject_quality_issues(data)

    assert isinstance(enriched, pd.DataFrame)
    assert "score_lecture" in enriched.columns
    assert enriched["score_lecture"].isna().sum() > 0
