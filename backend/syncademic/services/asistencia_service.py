from .models import Estudiante, Asignatura, Asistencia

def calcular_tasa_asistencia(estudiante, mes):
    # Calcula la tasa de asistencia para un estudiante en un mes específico
    total_clases = Asistencia.objects.filter(
        estudiante=estudiante,
        semana__gte=mes * 4 - 3,
        semana__lte=mes * 4
    ).count()
    clases_asistidas = Asistencia.objects.filter(
        estudiante=estudiante,
        presente=True,
        semana__gte=mes * 4 - 3,
        semana__lte=mes * 4
    ).count()
    return (clases_asistidas / total_clases) * 100 if total_clases > 0 else 0

def obtener_estudiantes_en_riesgo(mes):
    minimo = 0
    maximo = 70
    estudiantes_en_riesgo = []

    for estudiante in Estudiante.objects.all():
        tasa_asistencia = calcular_tasa_asistencia(estudiante, mes)
        if minimo <= tasa_asistencia <= maximo:
            estudiantes_en_riesgo.append({
                'nombre': estudiante.nombre,
                'tasa_asistencia': tasa_asistencia,
            })

    return estudiantes_en_riesgo

def actualizar_asistencia(estudiante_id, asignatura_id, semana, dia, presente):
    asistencia, created = Asistencia.objects.update_or_create(
        estudiante_id=estudiante_id,
        asignatura_id=asignatura_id,
        semana=semana,
        dia=dia,
        defaults={'presente': presente}
    )
    return asistencia, created