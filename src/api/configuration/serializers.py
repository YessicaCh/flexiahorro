from rest_framework import serializers
from apps.core.models import Level, SavingsGoal
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"  # Serializar todos los campos


class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = "__all__"

    def validate(self, data):
        """Validaciones en el serializer (se ejecutan antes de guardar)"""
        savings_mode = data.get("savings_mode")

        if savings_mode == "percentage" and not data.get("percentage_value"):
            raise serializers.ValidationError("Debe seleccionar un valor de porcentaje (5%, 10% o 15%).")
        if savings_mode == "fixed" and not data.get("fixed_amount"):
            raise serializers.ValidationError("Debe ingresar un monto fijo.")
        if savings_mode == "rounding" and not data.get("rounding_to"):
            raise serializers.ValidationError("Debe seleccionar si redondea al próximo 5 o 10.")
        if savings_mode == "range":
            range_start = data.get("range_start")
            range_end = data.get("range_end")
            if not range_start or not range_end:
                raise serializers.ValidationError("Debe ingresar valores de inicio y fin para el rango.")
            if range_start >= range_end:
                raise serializers.ValidationError("El valor de inicio debe ser menor al de fin.")

        return data


        
# class AppFaqSerializer(serializers.Serializer):
#     question = serializers.CharField()
#     answer = serializers.CharField()
    
# class AppUseTermSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()

# class LegalDocumentSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(source='name')
#     class Meta:
#         model = LegalDocument
#         fields = ('identifier','title','content','is_active')

# class LegalDocumentConfigSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LegalDocument
#         fields = ('identifier','is_active')

# class AppVersionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppVersion
#         fields = ('app_version', 'app_platform',
#                   'app_force_update', 'created_at')

# class FontSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Font
#         fields = ['family', 'weight']

# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = ['name', 'code']

# class StyleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Style
#         fields = ['css']

# class LogoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Logo
#         fields = ['name', 'image']
        
# class ThemeModeSerializer(serializers.ModelSerializer):
#     fonts = serializers.SerializerMethodField()
#     colors = serializers.SerializerMethodField()
#     styles = serializers.SerializerMethodField()
#     logos = serializers.SerializerMethodField()

#     class Meta:
#         model = ThemeMode
#         fields = ['mode', 'fonts', 'colors', 'styles', 'logos']

#     def get_fonts(self, obj):
#         fonts = obj.fonts.all()
#         font_data = {}
#         for font in fonts:
#             font_data[font.name] = {
#                 'family': font.family,
#                 'weight': font.weight
#             }
#         return font_data

#     def get_colors(self, obj):
#         colors = obj.colors.all()
#         color_data = {}
#         for color in colors:
#             color_data[color.name] = color.code
#         return color_data

#     def get_styles(self, obj):
#         styles = obj.styles
#         return {
#             'css': styles.css if styles else ''
#         }

#     def get_logos(self, obj):
#         logos = obj.logos.all()
#         logo_data = {}
#         for logo in logos:
#             #logo_data[logo.name] = str(logo.image)
#             if logo.image:
#                 logo_data[logo.name] =  f"{settings.MEDIA_URL}{str(logo.image)}"
#         return logo_data

# class PageBlockSerializer(serializers.Serializer):
#     identifier = serializers.CharField()
#     component_type = serializers.CharField()
#     #component_block = serializers.SerializerMethodField()
#     component_design = serializers.CharField()

#     def get_component_block(self, component):
#         print(f'PageBlockSerializer - get_component_block - {component}')
#         return f'page_component_{component["position"]}'

# class GlobalAppConfigSerializer(serializers.Serializer):
#     show_subcription = serializers.BooleanField(default=False) 
#     show_sala_plus = serializers.BooleanField(default=False)
#     show_menu_podcast = serializers.BooleanField(default=False)
#     show_menu_epaper = serializers.BooleanField(default=False)
#     url_suscription = serializers.CharField(default='', allow_blank=True)  
#     premium_identifier = serializers.CharField(default='', allow_blank=True)
#     has_subscription = serializers.BooleanField(default=False)
#     show_assistant = serializers.BooleanField(default=False)
    
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         services = settings.BASE_SETTINGS.get('services', [])
#         for service in services:
#             if service.get("service") == "podcast" and service.get("is_active"):
#                 representation["show_menu_podcast"] = True
#             elif service.get("service") == "epaper" and service.get("is_active"):
#                 representation["show_menu_epaper"] = True
#         return representation
      
# class AppConfigurationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppConfiguration
#         fields = ('logo', 'logo_2')

# class AppInitDataSerializer(serializers.Serializer):
#     app_menu = serializers.JSONField()
#     app_config = serializers.JSONField()
#     pages = serializers.JSONField()
#     services = ServiceListSerializer(many=True)


# class AppWelcomeSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     image = serializers.SerializerMethodField()

#     @extend_schema_field(
#         {
#             "type": "object",
#             "properties": {
#                 "url": {"type": "string", "example": "https://example.com/image.jpg"},
#                 "type": {"type": "string", "example": "JPG"}
#             }
#         }
#     )
#     def get_image(self, obj):
#         try:
#             image_data = obj.get('image')
#             if image_data is None:
#                 return {
#                     "url": "",
#                     "type": "",
#                 }
#             return {
#                 "url": obj['image']['url'],
#                 "type": obj['image']['type']
#             }
#         except Exception as e:
#             print(f"AppWelcomeSerializer - get_image - {e}")
#             return {
#                 "url": "",
#                 "type": ""
#             }


# class BreakingAlertSerializer(serializers.Serializer):
#     label = serializers.CharField()
#     label_color = serializers.CharField()
#     title = serializers.CharField()
#     url_type = serializers.CharField()
#     url = serializers.CharField()
#     is_publish = serializers.BooleanField()
