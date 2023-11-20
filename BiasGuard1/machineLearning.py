from .views import *
from .models import Offer
# -- MANEJO DE LENGUAJE NATURAL --
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string
import re
nltk.download('stopwords')

import joblib
modeloEdad = joblib.load('modeloSVM/modeloSVMEdad.pkl')
modeloGenero = joblib.load('modeloSVM/modeloSVMGenero.pkl')



def procesa_oferta(oferta):
    '''
    Limpiamos la oferta con información importante para entrenar los modelos
        input: oferta
        output: oferta limpia
    '''
    stopwords_spanish = stopwords.words('spanish')
    #Elimina puntuación
    oferta = re.sub(r'[^\w\s]', '', oferta)
    # tokenize oferta
    tokenizer = TweetTokenizer(preserve_case=False)
    oferta_tokens = tokenizer.tokenize(oferta)

    oferta_clean = []

    for word in oferta_tokens:
        if word not in stopwords_spanish and word not in string.punctuation:
            oferta_clean.append(word)

    return oferta_clean

def genera_caracteristicas(oferta, freqs):
    '''
    Input:
        oferta: descripción de la oferta
        freqs: diccionario de frecuencias
    Output:
        x: a feature vector of dimension (1,3)
    '''
    # Procesamos los tweets
    word_l = procesa_oferta(oferta)

    # una lista con 2 elementos
    x = [0, 0]

    # Para cada palabra en la lista de palabras tokenizadas
    for word in word_l:
        # El primer componente es la suma de las veces que aparece esa palabra en ofertas adecuadas
        x[0] += freqs.get((word, 1), 0)

        # El segundo componente es la suma de las veces que aparece esa palabra en ofertas discriminatorias
        x[1] += freqs.get((word, 0), 0)
    return x




def discriminacionGenero(description):
    oferta = genera_caracteristicas(description,frecuencias_genero)
    texto_ofensivo = modeloGenero.predict([oferta])
    palabras_discriminatorias = ['hombre','mujer','femenino','femenina','masculino','masculina','enfermera','limpiadora']
    palabras_encontradas = []
    print(texto_ofensivo[0])
    if texto_ofensivo[0]==False:
        palabras_texto = procesa_oferta(description)
        for palabra in palabras_discriminatorias:
            # Verificar si la palabra está en el texto
            if palabra in palabras_texto:
                palabras_encontradas.append(palabra)       

    return bool(texto_ofensivo[0]),palabras_encontradas



def discriminacionEdad(description):
    oferta = genera_caracteristicas(description,frecuencias_edad)
    texto_ofensivo = modeloEdad.predict([oferta])
    palabras_discriminatorias = ['años','joven','recién','graduado','juvenil','estudiante','graduada','30','menor']
    palabras_encontradas = []
    print(texto_ofensivo[0])
    if texto_ofensivo[0]==False:
        palabras_texto = procesa_oferta(description)
        for palabra in palabras_discriminatorias:
            # Verificar si la palabra está en el texto
            if palabra in palabras_texto:
                palabras_encontradas.append(palabra)       

    return bool(texto_ofensivo[0]),palabras_encontradas




frecuencias_edad = {('empresa', 1): 20, ('innovadora', 1): 4, ('busca', 1): 47, ('desarrollador', 1): 3, ('web', 1): 8, ('junior', 1): 6, ('unirse', 1): 2, ('equipo', 1): 6, ('valoramos', 1): 32, ('experiencia', 1): 60, ('lenguajes', 1): 5, ('programación', 1): 7, ('específicos', 1): 3, ('capacidad', 1): 20, ('trabajar', 1): 8, ('proyectos', 1): 25, ('desafiantes', 1): 3, ('necesita', 1): 6, ('enfermeroa', 1): 3, ('residencia', 1): 2, ('ancianos', 1): 2, ('buscamos', 1): 8, ('candidatosas', 1): 4, ('cuidado', 1): 3, ('personas', 1): 4, ('mayores', 1): 2, ('enfoque', 1): 6, ('compasivo', 1): 2, ('hacia', 1): 2, ('atención', 1): 11, ('salud', 1): 3, ('compañía', 1): 2, ('tecnología', 1): 5, ('programador', 1): 2, ('habilidades', 1): 50, ('entusiasmo', 1): 2, ('aprender', 1): 3, ('contribuir', 1): 6, ('desarrollo', 1): 13, ('software', 1): 13, ('vendedora', 1): 2, ('tienda', 1): 2, ('ropa', 1): 4, ('femenina', 1): 3, ('apasionadas', 1): 1, ('moda', 1): 9, ('excepcionales', 1): 3, ('cliente', 1): 9, ('importante', 1): 2, ('producción', 1): 2, ('audiovisual', 1): 2, ('editora', 1): 2, ('video', 1): 2, ('diseño', 1): 21, ('campañas', 1): 5, ('publicitarias', 1): 5, ('creativas', 1): 3, ('creatividad', 1): 12, ('sólidas', 1): 2, ('edición', 1): 2, ('consultoría', 1): 2, ('líder', 1): 4, ('analista', 1): 8, ('financieroa', 1): 3, ('realizar', 1): 5, ('análisis', 1): 8, ('reportes', 1): 2, ('financieros', 1): 4, ('individuos', 1): 2, ('fuertes', 1): 2, ('analíticas', 1): 2, ('interés', 1): 2, ('mundo', 1): 2, ('financiero', 1): 4, ('startup', 1): 5, ('desarrolladora', 1): 7, ('aplicaciones', 1): 10, ('móviles', 1): 6, ('creación', 1): 6, ('innovadoras', 1): 5, ('valoran', 1): 13, ('avanzadas', 1): 4, ('agencia', 1): 4, ('marketing', 1): 8, ('especialista', 1): 7, ('digital', 1): 5, ('diseñar', 1): 3, ('ejecutar', 1): 1, ('estrategias', 1): 3, ('efectivas', 1): 4, ('ámbito', 1): 3, ('ingenieroa', 1): 6, ('liderar', 1): 9, ('infraestructura', 1): 3, ('buscan', 1): 2, ('comprobada', 1): 3, ('similares', 1): 4, ('gestión', 1): 14, ('equipos', 1): 7, ('asistente', 1): 5, ('administrativoa', 1): 2, ('organizativas', 1): 4, ('directamente', 1): 2, ('gerencia', 1): 2, ('eficiencia', 1): 5, ('oficina', 1): 4, ('trabajo', 1): 2, ('diseñadora', 1): 6, ('urbana', 1): 2, ('crear', 1): 4, ('prendas', 1): 3, ('colecciones', 1): 4, ('únicas', 1): 3, ('contemporánea', 1): 2, ('alimentos', 1): 2, ('chef', 1): 4, ('pasteleroa', 1): 2, ('repostería', 1): 2, ('decoración', 1): 2, ('pasteles', 1): 2, ('culinaria', 1): 2, ('programadora', 1): 3, ('senior', 1): 2, ('liderazgo', 1): 6, ('sólida', 1): 2, ('gerente', 1): 2, ('multidisciplinarios', 1): 2, ('conductora', 1): 2, ('transporte', 1): 2, ('carga', 1): 2, ('licencia', 1): 6, ('manejo', 1): 4, ('vehículos', 1): 2, ('pesados', 1): 2, ('entregas', 1): 4, ('domicilio', 1): 4, ('seguridad', 1): 3, ('conducción', 1): 2, ('gimnasio', 1): 2, ('instructora', 1): 2, ('pesas', 1): 2, ('entrenamiento', 1): 2, ('fuerza', 1): 2, ('acondicionamiento', 1): 2, ('físico', 1): 2, ('pasión', 1): 2, ('fitness', 1): 2, ('instrucción', 1): 2, ('dinámico', 1): 1, ('html', 1): 3, ('css', 1): 3, ('javascript', 1): 3, ('así', 1): 2, ('enfrentar', 1): 1, ('nuevas', 1): 1, ('tecnologías', 1): 3, ('comprometidoa', 1): 1, ('médica', 1): 3, ('bienestar', 1): 1, ('residentes', 1): 1, ('clave', 1): 1, ('apasionadoa', 1): 1, ('fuerte', 1): 1, ('experiencias', 1): 2, ('compra', 1): 1, ('positivas', 1): 1, ('creativoa', 1): 2, ('ejecución', 1): 2, ('vanguardista', 1): 1, ('perspectiva', 1): 1, ('creativa', 1): 1, ('reconocida', 1): 1, ('innovar', 1): 1, ('pastelería', 1): 1, ('tecnológicos', 1): 2, ('ambiciosos', 1): 1, ('crecimiento', 1): 1, ('mentalidad', 1): 1, ('orientada', 1): 1, ('resultados', 1): 1, ('logística', 1): 2, ('seguro', 1): 1, ('prestigio', 1): 1, ('compromiso', 1): 1, ('vanguardia', 1): 1, ('proactivo', 1): 1, ('publicidad', 1): 2, ('gráficoa', 1): 2, ('gráfico', 1): 3, ('visual', 1): 1, ('comunicar', 1): 1, ('mensajes', 1): 2, ('impactantes', 1): 1, ('técnicoa', 1): 2, ('reparación', 1): 3, ('electrodomésticos', 1): 2, ('reparaciones', 1): 3, ('técnicas', 1): 3, ('orientado', 1): 1, ('servicio', 1): 2, ('estudio', 1): 2, ('abogados', 1): 1, ('legal', 1): 2, ('apoyar', 1): 1, ('labores', 1): 1, ('administrativas', 1): 1, ('legales', 1): 2, ('conocimiento', 1): 4, ('temas', 1): 1, ('meticuloso', 1): 1, ('documentación', 1): 1, ('recepcionista', 1): 1, ('hotel', 1): 1, ('reservas', 1): 1, ('cortesía', 1): 1, ('proporcionar', 1): 3, ('acogedora', 1): 1, ('huéspedes', 1): 1, ('transmitir', 1): 1, ('persuasivos', 1): 1, ('servicios', 1): 1, ('especializadoa', 1): 1, ('técnica', 1): 1, ('resolución', 1): 5, ('problemas', 1): 5, ('habilidad', 1): 3, ('modas', 1): 1, ('comprensión', 1): 1, ('tendencias', 1): 3, ('spa', 1): 1, ('lujo', 1): 1, ('esteticista', 1): 1, ('tratamientos', 1): 1, ('belleza', 1): 1, ('piel', 1): 1, ('masajes', 1): 1, ('ofrecer', 1): 2, ('relajantes', 1): 1, ('clientes', 1): 2, ('repartidora', 1): 1, ('puntualidad', 1): 1, ('mantener', 1): 4, ('calidad', 1): 1, ('accesorios', 1): 2, ('complementar', 1): 1, ('seguir', 1): 2, ('mercado', 1): 1, ('clínica', 1): 1, ('especializada', 1): 1, ('ginecólogoa', 1): 1, ('especializado', 1): 1, ('empatía', 1): 1, ('integral', 1): 1, ('móvile', 1): 1, ('consultora', 1): 2, ('empresariales', 1): 1, ('negocios', 1): 1, ('soluciones', 1): 1, ('construcción', 1): 2, ('civil', 1): 2, ('gestionar', 1): 1, ('reconocido', 1): 1, ('restaurante', 1): 1, ('alta', 1): 2, ('cocina', 1): 5, ('internacional', 1): 1, ('culinarias', 1): 1, ('presentación', 1): 1, ('platillos', 1): 1, ('full', 1): 3, ('stack', 1): 3, ('frontend', 1): 1, ('backend', 1): 1, ('específicas', 1): 1, ('jardín', 1): 1, ('infantes', 1): 1, ('maestroa', 1): 1, ('preescolar', 1): 1, ('cuidar', 1): 1, ('educar', 1): 1, ('niños', 1): 1, ('pequeños', 1): 1, ('enseñanza', 1): 1, ('paciencia', 1): 1, ('dedicación', 1): 1, ('infantil', 1): 1, ('textil', 1): 1, ('telas', 1): 1, ('nuevos', 1): 1, ('patrones', 1): 1, ('textiles', 1): 1, ('detalle', 1): 1, ('telecomunicaciones', 1): 1, ('redes', 1): 4, ('mantenimiento', 1): 1, ('infraestructuras', 1): 1, ('red', 1): 1, ('configuración', 1): 1, ('comunicación', 1): 2, ('persona', 1): 1, ('recursos', 1): 4, ('humanos', 1): 3, ('reclutamiento', 1): 2, ('capacitación', 1): 1, ('beneficios', 1): 1, ('licenciatura', 1): 2, ('campo', 1): 2, ('relacionado', 1): 2, ('planificación', 1): 3, ('línea', 1): 1, ('google', 1): 1, ('analytics', 1): 1, ('sociales', 1): 2, ('registradoa', 1): 1, ('válida', 1): 1, ('hospitalaria', 1): 1, ('capaz', 1): 1, ('directa', 1): 1, ('registros', 1): 1, ('precisos', 1): 1, ('interactivas', 1): 2, ('administrativo', 1): 1, ('dominio', 1): 2, ('datos', 1): 6, ('estadístico', 1): 2, ('bases', 1): 2, ('herramientas', 1): 3, ('sql', 1): 2, ('excel', 1): 2, ('ingeniero', 1): 2, ('eléctrico', 1): 1, ('conocimientos', 1): 12, ('sistemas', 1): 4, ('eléctricos', 1): 2, ('energía', 1): 2, ('renovable', 1): 2, ('profesional', 1): 4, ('asesor', 1): 1, ('certificación', 1): 2, ('financiera', 1): 2, ('carteras', 1): 2, ('sólidos', 1): 2, ('productos', 1): 2, ('diseñador', 1): 1, ('excepcional', 1): 1, ('adobe', 1): 1, ('creative', 1): 1, ('suite', 1): 1, ('materiales', 1): 1, ('visuales', 1): 1, ('soporte', 1): 2, ('técnico', 1): 2, ('hardware', 1): 2, ('operativos', 1): 2, ('ejecutivo', 1): 1, ('inventario', 1): 1, ('costos', 1): 1, ('apps', 1): 1, ('ios', 1): 1, ('android', 1): 1, ('swift', 1): 1, ('kotlin', 1): 1, ('información', 1): 1, ('evaluación', 1): 1, ('riesgos', 1): 1, ('implementación', 1): 1, ('medidas', 1): 1, ('ciberseguridad', 1): 1, ('contenidos', 1): 1, ('contenido', 1): 1, ('seo', 1): 1, ('supervisión', 1): 1, ('naturales', 1): 1, ('investigación', 1): 2, ('ambiental', 1): 1, ('recopilación', 1): 2, ('relacionados', 1): 1, ('medio', 1): 1, ('ambiente', 1): 1, ('científica', 1): 1, ('experimental', 1): 1, ('laboratorios', 1): 1, ('mejora', 1): 1, ('continua', 1): 1, ('finanzas', 1): 1, ('corporativas', 1): 1, ('modelado', 1): 1, ('inversiones', 1): 1, ('valoración', 1): 1, ('empresas', 1): 1, ('diversidad', 1): 1, ('inclusión', 1): 1, ('talento', 1): 1, ('eléctricoa', 1): 1, ('asesora', 1): 1, ('buscamos', 0): 13, ('estudiante', 0): 1, ('universitario', 0): 1, ('recién', 0): 3, ('graduado', 0): 3, ('preferiblemente', 0): 22, ('menor', 0): 80, ('25', 0): 11, ('años', 0): 82, ('profesional', 0): 2, ('enérgico', 0): 3, ('40', 0): 1, ('menos', 0): 2, ('10', 0): 1, ('experiencia', 0): 14, ('campo', 0): 2, ('enfocamos', 0): 1, ('encontrar', 0): 1, ('alguien', 0): 5, ('joven', 0): 32, ('lleno', 0): 1, ('ideas', 0): 1, ('frescas', 0): 1, ('liderar', 0): 3, ('equipo', 0): 8, ('busca', 0): 64, ('camarero', 0): 1, ('restaurante', 0): 2, ('lujo', 0): 1, ('candidato', 0): 3, ('30', 0): 21, ('actitud', 0): 2, ('entusiasta', 0): 2, ('capacidad', 0): 2, ('trabajar', 0): 1, ('entorno', 0): 2, ('ritmo', 0): 1, ('rápido', 0): 1, ('programador', 0): 5, ('informático', 0): 1, ('unirse', 0): 2, ('desarrollo', 0): 11, ('preferimos', 0): 6, ('poca', 0): 1, ('laboral', 0): 1, ('28', 0): 12, ('persona', 0): 4, ('dinámica', 0): 3, ('creativa', 0): 1, ('enérgica', 0): 1, ('35', 0): 2, ('cinco', 0): 1, ('agencias', 0): 1, ('renombre', 0): 1, ('queremos', 0): 3, ('líder', 0): 2, ('impulsar', 0): 3, ('departamento', 0): 1, ('cuentas', 0): 3, ('apariencia', 0): 1, ('fresca', 0): 4, ('salido', 0): 1, ('universidad', 0): 1, ('27', 0): 12, ('perfil', 0): 2, ('adaptable', 0): 1, ('constante', 0): 1, ('evolución', 0): 1, ('recientemente', 0): 1, ('talentoso', 0): 1, ('diseñador', 0): 5, ('32', 0): 2, ('cartera', 0): 1, ('proyectos', 0): 8, ('vanguardia', 0): 1, ('visionario', 0): 1, ('imagen', 0): 1, ('marca', 0): 3, ('desarrollador', 0): 2, ('proactivo', 0): 1, ('29', 0): 7, ('aplicaciones', 0): 4, ('móviles', 0): 3, ('vendedor', 0): 3, ('tienda', 0): 5, ('moda', 0): 9, ('26', 0): 12, ('pasión', 0): 4, ('atención', 0): 5, ('cliente', 0): 6, ('representar', 0): 1, ('startup', 0): 8, ('crecimiento', 0): 1, ('gerente', 0): 3, ('operaciones', 0): 1, ('dinámico', 0): 1, ('habilidades', 0): 11, ('gestión', 0): 1, ('comprobadas', 0): 1, ('valoramos', 0): 3, ('juventud', 0): 3, ('creatividad', 0): 4, ('dirigir', 0): 1, ('redactor', 0): 4, ('contenido', 0): 11, ('digital', 0): 6, ('creativo', 0): 6, ('creación', 0): 3, ('online', 0): 3, ('aporte', 0): 1, ('perspectiva', 0): 1, ('estrategia', 0): 1, ('agencia', 0): 17, ('viajes', 0): 6, ('agente', 0): 4, ('reservas', 0): 6, ('comunicación', 0): 1, ('excepcionales', 0): 1, ('entusiasmo', 0): 2, ('necesita', 0): 8, ('chef', 0): 4, ('alta', 0): 1, ('cocina', 0): 1, ('culinaria', 0): 1, ('gastronomía', 0): 1, ('moderna', 0): 1, ('innovador', 0): 1, ('empresa', 0): 16, ('eventos', 0): 9, ('coordinador', 0): 3, ('junior', 0): 35, ('organización', 0): 1, ('especialista', 0): 4, ('marketing', 0): 9, ('estrategias', 0): 7, ('redes', 0): 4, ('sociales', 0): 4, ('publicidad', 0): 7, ('gráfico', 0): 5, ('crear', 0): 3, ('visual', 0): 1, ('fresco', 0): 1, ('atractivo', 0): 2, ('web', 0): 10, ('preferentemente', 0): 15, ('innovadores', 0): 4, ('tecnología', 0): 4, ('asistente', 0): 4, ('ventas', 0): 3, ('comunicativas', 0): 1, ('producto', 0): 1, ('lanzamiento', 0): 1, ('nuevos', 0): 1, ('servicios', 0): 1, ('seo', 0): 3, ('software', 0): 3, ('técnico', 0): 3, ('soporte', 0): 3, ('brindar', 0): 1, ('asistencia', 0): 1, ('técnica', 0): 1, ('clientes', 0): 4, ('planificar', 0): 1, ('ejecutar', 0): 1, ('campañas', 0): 5, ('creativas', 0): 3, ('fotógrafoa', 0): 3, ('editoriales', 0): 1, ('comerciales', 0): 2, ('consultoría', 0): 3, ('administrativo', 0): 1, ('multitarea', 0): 1, ('organizativas', 0): 1, ('excelente', 0): 1, ('servicio', 0): 1, ('innovación', 0): 1, ('analista', 0): 7, ('datos', 0): 3, ('analíticas', 0): 1, ('interpretar', 0): 1, ('tendencias', 0): 3, ('electrónica', 0): 1, ('conocimientos', 0): 2, ('tecnológicos', 0): 1, ('últimas', 0): 1, ('community', 0): 3, ('manager', 0): 3, ('gestionar', 0): 3, ('entretenimiento', 0): 1, ('diseño', 0): 6, ('ilustradora', 0): 1, ('visuales', 0): 4, ('únicos', 0): 1, ('estudio', 0): 1, ('arquitectura', 0): 1, ('arquitectoa', 0): 2, ('desarrolladora', 0): 1, ('experiencias', 0): 1, ('interactivas', 0): 1, ('planificadora', 0): 1, ('medios', 0): 1, ('producción', 0): 1, ('audiovisual', 0): 2, ('editora', 0): 2, ('video', 0): 2, ('contar', 0): 1, ('historias', 0): 1, ('comercio', 0): 2, ('electrónico', 0): 1, ('realizar', 0): 3, ('análisis', 0): 4, ('estadísticos', 0): 2, ('investigación', 0): 2, ('ejecutivo', 0): 2, ('manejar', 0): 4, ('relaciones', 0): 2, ('publicitarias', 0): 6, ('apps', 0): 2, ('móvil', 0): 2, ('ios', 0): 2, ('android', 0): 2, ('modelo', 0): 2, ('desfiles', 0): 2, ('electrónicos', 0): 2, ('técnicos', 0): 2, ('productos', 0): 2, ('recursos', 0): 1, ('humanos', 0): 1, ('apoyar', 0): 2, ('procesos', 0): 1, ('selección', 0): 1, ('capacitación', 0): 1, ('uxui', 0): 2, ('mejorar', 0): 4, ('usuario', 0): 2, ('alimentos', 0): 2, ('desarrollar', 0): 5, ('nuevas', 0): 2, ('recetas', 0): 2, ('menús', 0): 1, ('organizador', 0): 1, ('coordinar', 0): 1, ('celebraciones', 0): 1, ('conferencias', 0): 1, ('optimizar', 0): 1, ('posicionamiento', 0): 1, ('resolver', 0): 2, ('problemas', 0): 2, ('sesiones', 0): 2, ('fotográficas', 0): 2, ('producciones', 0): 1, ('interiores', 0): 1, ('exteriores', 0): 1, ('mantener', 0): 2, ('sitios', 0): 2, ('videojuegos', 0): 2, ('tester', 0): 2, ('probar', 0): 2, ('reportar', 0): 1, ('errores', 0): 1, ('juegos', 0): 2, ('ofrecer', 0): 1, ('editar', 0): 1, ('financiero', 0): 2, ('proyecciones', 0): 1, ('financieras', 0): 1, ('llevar', 0): 1, ('cabo', 0): 1, ('línea', 0): 2, ('materiales', 0): 1, ('actuales', 0): 1, ('iniciativas', 0): 1, ('innovadoras', 0): 1, ('redacción', 0): 2, ('visibilidad', 0): 1, ('funcionalidad', 0): 1, ('talento', 0): 1, ('conceptualizar', 0): 1, ('diseñar', 0): 1, ('plataformas', 0): 1, ('conceptos', 0): 1, ('gastronómicos', 0): 1, ('organizar', 0): 1, ('corporativos', 0): 1, ('redactora', 0): 1, ('publicitaria', 0): 1, ('estratega', 0): 1, ('colecciones', 0): 1, ('programadora', 0): 1, ('reportes', 0): 1, ('financieros', 0): 1}


frecuencias_genero = {('empresa', 1): 20, ('innovadora', 1): 4, ('busca', 1): 47, ('desarrollador', 1): 3, ('web', 1): 8, ('junior', 1): 6, ('unirse', 1): 2, ('equipo', 1): 6, ('valoramos', 1): 32, ('experiencia', 1): 60, ('lenguajes', 1): 5, ('programación', 1): 7, ('específicos', 1): 3, ('capacidad', 1): 20, ('trabajar', 1): 8, ('proyectos', 1): 25, ('desafiantes', 1): 3, ('necesita', 1): 6, ('enfermeroa', 1): 3, ('residencia', 1): 2, ('ancianos', 1): 2, ('buscamos', 1): 8, ('candidatosas', 1): 4, ('cuidado', 1): 3, ('personas', 1): 4, ('mayores', 1): 2, ('enfoque', 1): 6, ('compasivo', 1): 2, ('hacia', 1): 2, ('atención', 1): 11, ('salud', 1): 3, ('compañía', 1): 2, ('tecnología', 1): 5, ('programador', 1): 2, ('habilidades', 1): 50, ('entusiasmo', 1): 2, ('aprender', 1): 3, ('contribuir', 1): 6, ('desarrollo', 1): 13, ('software', 1): 13, ('vendedora', 1): 2, ('tienda', 1): 2, ('ropa', 1): 4, ('femenina', 1): 3, ('apasionadas', 1): 1, ('moda', 1): 9, ('excepcionales', 1): 3, ('cliente', 1): 9, ('importante', 1): 2, ('producción', 1): 2, ('audiovisual', 1): 2, ('editora', 1): 2, ('video', 1): 2, ('diseño', 1): 21, ('campañas', 1): 5, ('publicitarias', 1): 5, ('creativas', 1): 3, ('creatividad', 1): 12, ('sólidas', 1): 2, ('edición', 1): 2, ('consultoría', 1): 2, ('líder', 1): 4, ('analista', 1): 8, ('financieroa', 1): 3, ('realizar', 1): 5, ('análisis', 1): 8, ('reportes', 1): 2, ('financieros', 1): 4, ('individuos', 1): 2, ('fuertes', 1): 2, ('analíticas', 1): 2, ('interés', 1): 2, ('mundo', 1): 2, ('financiero', 1): 4, ('startup', 1): 5, ('desarrolladora', 1): 7, ('aplicaciones', 1): 10, ('móviles', 1): 6, ('creación', 1): 6, ('innovadoras', 1): 5, ('valoran', 1): 13, ('avanzadas', 1): 4, ('agencia', 1): 4, ('marketing', 1): 8, ('especialista', 1): 7, ('digital', 1): 5, ('diseñar', 1): 3, ('ejecutar', 1): 1, ('estrategias', 1): 3, ('efectivas', 1): 4, ('ámbito', 1): 3, ('ingenieroa', 1): 6, ('liderar', 1): 9, ('infraestructura', 1): 3, ('buscan', 1): 2, ('comprobada', 1): 3, ('similares', 1): 4, ('gestión', 1): 14, ('equipos', 1): 7, ('asistente', 1): 5, ('administrativoa', 1): 2, ('organizativas', 1): 4, ('directamente', 1): 2, ('gerencia', 1): 2, ('eficiencia', 1): 5, ('oficina', 1): 4, ('trabajo', 1): 2, ('diseñadora', 1): 6, ('urbana', 1): 2, ('crear', 1): 4, ('prendas', 1): 3, ('colecciones', 1): 4, ('únicas', 1): 3, ('contemporánea', 1): 2, ('alimentos', 1): 2, ('chef', 1): 4, ('pasteleroa', 1): 2, ('repostería', 1): 2, ('decoración', 1): 2, ('pasteles', 1): 2, ('culinaria', 1): 2, ('programadora', 1): 3, ('senior', 1): 2, ('liderazgo', 1): 6, ('sólida', 1): 2, ('gerente', 1): 2, ('multidisciplinarios', 1): 2, ('conductora', 1): 2, ('transporte', 1): 2, ('carga', 1): 2, ('licencia', 1): 6, ('manejo', 1): 4, ('vehículos', 1): 2, ('pesados', 1): 2, ('entregas', 1): 4, ('domicilio', 1): 4, ('seguridad', 1): 3, ('conducción', 1): 2, ('gimnasio', 1): 2, ('instructora', 1): 2, ('pesas', 1): 2, ('entrenamiento', 1): 2, ('fuerza', 1): 2, ('acondicionamiento', 1): 2, ('físico', 1): 2, ('pasión', 1): 2, ('fitness', 1): 2, ('instrucción', 1): 2, ('dinámico', 1): 1, ('html', 1): 3, ('css', 1): 3, ('javascript', 1): 3, ('así', 1): 2, ('enfrentar', 1): 1, ('nuevas', 1): 1, ('tecnologías', 1): 3, ('comprometidoa', 1): 1, ('médica', 1): 3, ('bienestar', 1): 1, ('residentes', 1): 1, ('clave', 1): 1, ('apasionadoa', 1): 1, ('fuerte', 1): 1, ('experiencias', 1): 2, ('compra', 1): 1, ('positivas', 1): 1, ('creativoa', 1): 2, ('ejecución', 1): 2, ('vanguardista', 1): 1, ('perspectiva', 1): 1, ('creativa', 1): 1, ('reconocida', 1): 1, ('innovar', 1): 1, ('pastelería', 1): 1, ('tecnológicos', 1): 2, ('ambiciosos', 1): 1, ('crecimiento', 1): 1, ('mentalidad', 1): 1, ('orientada', 1): 1, ('resultados', 1): 1, ('logística', 1): 2, ('seguro', 1): 1, ('prestigio', 1): 1, ('compromiso', 1): 1, ('vanguardia', 1): 1, ('proactivo', 1): 1, ('publicidad', 1): 2, ('gráficoa', 1): 2, ('gráfico', 1): 3, ('visual', 1): 1, ('comunicar', 1): 1, ('mensajes', 1): 2, ('impactantes', 1): 1, ('técnicoa', 1): 2, ('reparación', 1): 3, ('electrodomésticos', 1): 2, ('reparaciones', 1): 3, ('técnicas', 1): 3, ('orientado', 1): 1, ('servicio', 1): 2, ('estudio', 1): 2, ('abogados', 1): 1, ('legal', 1): 2, ('apoyar', 1): 1, ('labores', 1): 1, ('administrativas', 1): 1, ('legales', 1): 2, ('conocimiento', 1): 4, ('temas', 1): 1, ('meticuloso', 1): 1, ('documentación', 1): 1, ('recepcionista', 1): 1, ('hotel', 1): 1, ('reservas', 1): 1, ('cortesía', 1): 1, ('proporcionar', 1): 3, ('acogedora', 1): 1, ('huéspedes', 1): 1, ('transmitir', 1): 1, ('persuasivos', 1): 1, ('servicios', 1): 1, ('especializadoa', 1): 1, ('técnica', 1): 1, ('resolución', 1): 5, ('problemas', 1): 5, ('habilidad', 1): 3, ('modas', 1): 1, ('comprensión', 1): 1, ('tendencias', 1): 3, ('spa', 1): 1, ('lujo', 1): 1, ('esteticista', 1): 1, ('tratamientos', 1): 1, ('belleza', 1): 1, ('piel', 1): 1, ('masajes', 1): 1, ('ofrecer', 1): 2, ('relajantes', 1): 1, ('clientes', 1): 2, ('repartidora', 1): 1, ('puntualidad', 1): 1, ('mantener', 1): 4, ('calidad', 1): 1, ('accesorios', 1): 2, ('complementar', 1): 1, ('seguir', 1): 2, ('mercado', 1): 1, ('clínica', 1): 1, ('especializada', 1): 1, ('ginecólogoa', 1): 1, ('especializado', 1): 1, ('empatía', 1): 1, ('integral', 1): 1, ('móvile', 1): 1, ('consultora', 1): 2, ('empresariales', 1): 1, ('negocios', 1): 1, ('soluciones', 1): 1, ('construcción', 1): 2, ('civil', 1): 2, ('gestionar', 1): 1, ('reconocido', 1): 1, ('restaurante', 1): 1, ('alta', 1): 2, ('cocina', 1): 5, ('internacional', 1): 1, ('culinarias', 1): 1, ('presentación', 1): 1, ('platillos', 1): 1, ('full', 1): 3, ('stack', 1): 3, ('frontend', 1): 1, ('backend', 1): 1, ('específicas', 1): 1, ('jardín', 1): 1, ('infantes', 1): 1, ('maestroa', 1): 1, ('preescolar', 1): 1, ('cuidar', 1): 1, ('educar', 1): 1, ('niños', 1): 1, ('pequeños', 1): 1, ('enseñanza', 1): 1, ('paciencia', 1): 1, ('dedicación', 1): 1, ('infantil', 1): 1, ('textil', 1): 1, ('telas', 1): 1, ('nuevos', 1): 1, ('patrones', 1): 1, ('textiles', 1): 1, ('detalle', 1): 1, ('telecomunicaciones', 1): 1, ('redes', 1): 4, ('mantenimiento', 1): 1, ('infraestructuras', 1): 1, ('red', 1): 1, ('configuración', 1): 1, ('comunicación', 1): 2, ('persona', 1): 1, ('recursos', 1): 4, ('humanos', 1): 3, ('reclutamiento', 1): 2, ('capacitación', 1): 1, ('beneficios', 1): 1, ('licenciatura', 1): 2, ('campo', 1): 2, ('relacionado', 1): 2, ('planificación', 1): 3, ('línea', 1): 1, ('google', 1): 1, ('analytics', 1): 1, ('sociales', 1): 2, ('registradoa', 1): 1, ('válida', 1): 1, ('hospitalaria', 1): 1, ('capaz', 1): 1, ('directa', 1): 1, ('registros', 1): 1, ('precisos', 1): 1, ('interactivas', 1): 2, ('administrativo', 1): 1, ('dominio', 1): 2, ('datos', 1): 6, ('estadístico', 1): 2, ('bases', 1): 2, ('herramientas', 1): 3, ('sql', 1): 2, ('excel', 1): 2, ('ingeniero', 1): 2, ('eléctrico', 1): 1, ('conocimientos', 1): 12, ('sistemas', 1): 4, ('eléctricos', 1): 2, ('energía', 1): 2, ('renovable', 1): 2, ('profesional', 1): 4, ('asesor', 1): 1, ('certificación', 1): 2, ('financiera', 1): 2, ('carteras', 1): 2, ('sólidos', 1): 2, ('productos', 1): 2, ('diseñador', 1): 1, ('excepcional', 1): 1, ('adobe', 1): 1, ('creative', 1): 1, ('suite', 1): 1, ('materiales', 1): 1, ('visuales', 1): 1, ('soporte', 1): 2, ('técnico', 1): 2, ('hardware', 1): 2, ('operativos', 1): 2, ('ejecutivo', 1): 1, ('inventario', 1): 1, ('costos', 1): 1, ('apps', 1): 1, ('ios', 1): 1, ('android', 1): 1, ('swift', 1): 1, ('kotlin', 1): 1, ('información', 1): 1, ('evaluación', 1): 1, ('riesgos', 1): 1, ('implementación', 1): 1, ('medidas', 1): 1, ('ciberseguridad', 1): 1, ('contenidos', 1): 1, ('contenido', 1): 1, ('seo', 1): 1, ('supervisión', 1): 1, ('naturales', 1): 1, ('investigación', 1): 2, ('ambiental', 1): 1, ('recopilación', 1): 2, ('relacionados', 1): 1, ('medio', 1): 1, ('ambiente', 1): 1, ('científica', 1): 1, ('experimental', 1): 1, ('laboratorios', 1): 1, ('mejora', 1): 1, ('continua', 1): 1, ('finanzas', 1): 1, ('corporativas', 1): 1, ('modelado', 1): 1, ('inversiones', 1): 1, ('valoración', 1): 1, ('empresas', 1): 1, ('diversidad', 1): 1, ('inclusión', 1): 1, ('talento', 1): 1, ('eléctricoa', 1): 1, ('asesora', 1): 1, ('busca', 0): 67, ('secretaria', 0): 3, ('oficina', 0): 3, ('preferiblemente', 0): 44, ('mujer', 0): 25, ('habilidades', 0): 19, ('organizativas', 0): 3, ('capacidad', 0): 1, ('asistir', 0): 1, ('altos', 0): 1, ('ejecutivos', 0): 1, ('empresa', 0): 18, ('diseño', 0): 10, ('diseñador', 0): 3, ('gráfico', 0): 1, ('masculino', 0): 14, ('ambiente', 0): 1, ('creativo', 0): 2, ('enérgico', 0): 1, ('necesita', 0): 13, ('enfermera', 0): 3, ('residencia', 0): 1, ('ancianos', 0): 1, ('experiencia', 0): 23, ('cuidado', 0): 3, ('personas', 0): 1, ('mayores', 0): 1, ('compañía', 0): 2, ('tecnología', 0): 6, ('programador', 0): 3, ('junior', 0): 1, ('preferentemente', 0): 5, ('hombre', 0): 24, ('lenguajes', 0): 3, ('programación', 0): 6, ('específicos', 0): 1, ('vendedora', 0): 2, ('tienda', 0): 2, ('ropa', 0): 4, ('femenina', 0): 8, ('pasión', 0): 2, ('moda', 0): 6, ('atención', 0): 8, ('cliente', 0): 7, ('construcción', 0): 1, ('obrero', 0): 2, ('realizar', 0): 6, ('trabajos', 0): 2, ('carga', 0): 4, ('descarga', 0): 2, ('maestra', 0): 1, ('preescolar', 0): 1, ('jardín', 0): 1, ('infantes', 0): 1, ('cuidar', 0): 1, ('educar', 0): 1, ('niños', 0): 1, ('pequeños', 0): 1, ('fábrica', 0): 1, ('operario', 0): 1, ('manejo', 0): 3, ('maquinaria', 0): 1, ('pesada', 0): 1, ('agencia', 0): 9, ('marketing', 0): 3, ('ejecutivo', 0): 2, ('cuentas', 0): 2, ('femenino', 0): 2, ('gestionar', 0): 2, ('estrategias', 0): 4, ('publicitarias', 0): 6, ('chef', 0): 6, ('restaurante', 0): 4, ('alta', 0): 4, ('cocina', 0): 5, ('internacional', 0): 1, ('startup', 0): 11, ('gerente', 0): 3, ('proyectos', 0): 11, ('liderar', 0): 10, ('equipos', 0): 3, ('multidisciplinarios', 0): 3, ('conductor', 0): 2, ('transporte', 0): 3, ('licencia', 0): 2, ('vehículos', 0): 2, ('pesados', 0): 2, ('estudio', 0): 4, ('abogados', 0): 1, ('asistente', 0): 4, ('legal', 0): 2, ('apoyar', 0): 2, ('labores', 0): 2, ('administrativas', 0): 2, ('legales', 0): 2, ('viajes', 0): 2, ('agente', 0): 3, ('reservas', 0): 8, ('manejar', 0): 3, ('desarrollador', 0): 5, ('web', 0): 2, ('avanzados', 0): 2, ('gimnasio', 0): 2, ('instructor', 0): 2, ('pesas', 0): 2, ('entrenamiento', 0): 2, ('fuerza', 0): 2, ('acondicionamiento', 0): 2, ('físico', 0): 2, ('recepcionista', 0): 2, ('hotel', 0): 2, ('gestión', 0): 4, ('publicidad', 0): 6, ('diseñadora', 0): 5, ('gráfica', 0): 4, ('trabajar', 0): 4, ('campañas', 0): 4, ('creativas', 0): 2, ('técnico', 0): 1, ('reparación', 0): 1, ('electrodomésticos', 0): 1, ('reparaciones', 0): 1, ('domicilio', 0): 4, ('consultoría', 0): 3, ('analista', 0): 3, ('financiera', 0): 3, ('análisis', 0): 3, ('reportes', 0): 3, ('financieros', 0): 3, ('barman', 0): 1, ('club', 0): 1, ('nocturno', 0): 1, ('coctelería', 0): 1, ('clínica', 0): 3, ('ginecólogo', 0): 2, ('salud', 0): 3, ('desarrolladora', 0): 2, ('aplicaciones', 0): 7, ('móviles', 0): 2, ('desarrollar', 0): 2, ('innovadoras', 0): 2, ('ingeniero', 0): 5, ('software', 0): 5, ('desarrollo', 0): 4, ('esteticista', 0): 2, ('spa', 0): 2, ('tratamientos', 0): 2, ('belleza', 0): 2, ('logística', 0): 2, ('repartidor', 0): 3, ('entregas', 0): 3, ('modas', 0): 3, ('crear', 0): 6, ('prendas', 0): 3, ('colecciones', 0): 3, ('únicas', 0): 3, ('técnica', 0): 2, ('radiología', 0): 2, ('imágenes', 0): 2, ('médicas', 0): 2, ('redactor', 0): 1, ('escribir', 0): 1, ('contenido', 0): 1, ('persuasivo', 0): 1, ('atractivo', 0): 1, ('alimentos', 0): 2, ('pastelera', 0): 2, ('repostería', 0): 2, ('decoración', 0): 2, ('pasteles', 0): 2, ('senior', 0): 2, ('liderazgo', 0): 2, ('equipo', 0): 2, ('infraestructura', 0): 3, ('prefiere', 0): 12, ('candidato', 0): 10, ('similares', 0): 3, ('administrativa', 0): 2, ('directamente', 0): 2, ('gerencia', 0): 2, ('director', 0): 2, ('comprobada', 0): 2, ('campo', 0): 2, ('pacientes', 0): 2, ('hospitalizados', 0): 2, ('cuidados', 0): 2, ('intensivos', 0): 2, ('creativa', 0): 2, ('candidata', 0): 2, ('visión', 0): 2, ('innovadora', 0): 2, ('vanguardia', 0): 3, ('avanzadas', 0): 3, ('apoyo', 0): 2, ('administrativo', 0): 2, ('conocimientos', 0): 2, ('urbana', 0): 2, ('contemporánea', 0): 2, ('culinarias', 0): 3, ('excepcionales', 0): 3, ('eventos', 0): 3, ('coordinador', 0): 1, ('planificar', 0): 1, ('ejecutar', 0): 1, ('laboratorio', 0): 1, ('centro', 0): 1, ('mental', 0): 1, ('psicólogo', 0): 1, ('terapia', 0): 1, ('cognitivoconductual', 0): 1, ('banco', 0): 1, ('manufactura', 0): 1, ('client', 0): 1}
