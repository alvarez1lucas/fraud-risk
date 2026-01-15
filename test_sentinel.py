
import pytest
import torch
import numpy as np

def test_model_output_shape():
    # Verifica que el modelo devuelva el formato correcto
    from app import SentinelFusionNet # Simulado
    m = SentinelFusionNet()
    x_tab = torch.randn(1, 2)
    x_bio = torch.randn(1, 2)
    out = m(x_tab, x_bio)
    assert out.shape == (1, 1)

def test_risk_logic():
    # Verifica que un deepfake score alto aumente el riesgo
    from app import analyze_risk
    low_risk = analyze_risk(100, "Mobile", 5, 0.8, 0.1)
    high_risk = analyze_risk(10000, "Emulator", 40, 0.1, 0.9)
    assert high_risk > low_risk
    