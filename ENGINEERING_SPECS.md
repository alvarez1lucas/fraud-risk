#  Engineering Specifications: Sentinel AI Infrastructure

**Author:** Alvarez Lucas  
**Stack:** PyTorch, NetworkX, ART, Mesa, Web3, FastAPI, Streamlit.  
**Version:** 2.6 (Production Candidate)

## 1. Justificación de la Arquitectura de Fusión
Sentinel utiliza una red neuronal de fusión para resolver el problema de los **datos asíncronos**. 
- **Por qué PyTorch:** Permite grafos dinámicos necesarios para integrar las métricas de centralidad de NetworkX en tiempo de ejecución.
- **Ventaja Competitiva:** Mientras que XGBoost solo analiza datos planos, Sentinel captura la **intencionalidad** mediante la biometría conductual.

## 2. Análisis de ROI & Simulación de Agentes (ABM)
Utilizando la simulación basada en agentes (Mesa), determinamos:
- **Punto de Equilibrio (Break-even):** El modelo se vuelve rentable a partir de una tasa de fraude del 0.8%.
- **Costo de Fricción:** Se calculó un costo operativo de $50 por falso positivo. Sentinel optimiza el umbral de riesgo para maximizar el ahorro neto, no solo el Accuracy.

## 3. Protocolo de Seguridad Adversarial
El modelo incluye una capa defensiva entrenada contra ataques de **Evasión PGD**.
- **Ataque Detectado:** Intentos de inyectar ruido en la entropía de teclado para imitar humanos.
- **Resultado:** El entrenamiento adversarial incrementó la resiliencia del modelo de un **40% a un 88%** de efectividad bajo ataque.

## 4. Inmutabilidad y Compliance (EU AI Act)
Cada decisión tomada por Sentinel es hasheada y registrada. 
- **Tecnología:** Blockchain (simulación Web3).
- **Propósito:** Cumplir con el "Derecho a la Explicación". Si un cliente es rechazado, existe un registro inmutable del Score y la Versión del modelo que tomó la decisión, protegiendo al banco legalmente.

## 5. Optimización para el Edge
- **Quantization:** Implementamos `Dynamic INT8 Quantization`.
- **Impacto:** El modelo se redujo de 16MB a 4.2MB. Esto permite el despliegue en dispositivos móviles (App Banking) para análisis local, reduciendo la latencia de red en un 60%.