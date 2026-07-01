from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY

# Metrics
patients_registered = Counter('patients_registered_total', 'Total patients registered')
waiting_patients = Gauge('waiting_patients', 'Current waiting patients')
triage_duration = Histogram('triage_duration_seconds', 'Triage classification time')
bed_occupancy = Gauge('bed_occupancy', 'Current bed occupancy')


def setup_metrics():
    """Metrics endpoint uchun"""
    from fastapi import Response

    async def metrics():
        return Response(generate_latest(REGISTRY), media_type="text/plain")

    return metrics