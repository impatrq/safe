import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/back_arrow_scaffold.dart';
import 'package:safe_app/components/customWidgets/url_launcher_icon.dart';
import 'package:safe_app/utilities/constants.dart';

class AboutUsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BackArrowScaffold(
      body: SingleChildScrollView(
        physics: BouncingScrollPhysics(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            BigDivider(),
            Row(
              children: [
                Image.asset('assets/images/safe_logo.png', width: 150.0, height: 150.0,),
                Expanded(
                  child: FittedBox(
                    fit: BoxFit.fitWidth,
                    child: Text(
                      'SAFE',
                      style: kBrandTitleYellowTextStyle,
                    ),
                  ),
                ),
              ],
            ),
            BigDivider(),
            Text('¿Quiénes somos?', style: kLittleTitleTextStyle,),
            SizedBox(height: 5.0,),
            Text(
              'Somos un equipo de estudiantes de la E.E.S.T. N.º 7 Taller Regional Quilmes (IMPA). En el marco de las Prácticas Profesionalizantes, desarrollamos un proyecto de fin de carrera, que ofrece una solución tecnológica que previene afecciones en el ámbito laboral.',
              style: kLittleGreyTextStyle.copyWith(fontSize: 20.0),
              textAlign: TextAlign.justify,
            ),
            BigDivider(),
            Text('¿Qué es SAFE?', style: kLittleTitleTextStyle,),
            SizedBox(height: 5.0,),
            Text(
              'S.A.F.E. (Secure Access For Environments) es un sistema que permite prevenir afecciones profesionales en el ámbito laboral.\n\nS.A.F.E. ofrece un control automatizado del acceso de los trabajadores a su área laboral, monitoreando las medidas de seguridad que ellos deben cumplir. Además lleva un registro en tiempo real de la ventilación y calidad del aire del ambiente de trabajo.\n\nDebido a la situación sanitaria que atravesamos, decidimos implementar controles con criterios epidemiológicos a fin de evitar la propagación del SARS-COV-2.',
              style: kLittleGreyTextStyle.copyWith(fontSize: 20.0),
              textAlign: TextAlign.justify,
            ),
            BigDivider(),
            Text('Beneficios', style: kLittleTitleTextStyle,),
            SizedBox(height: 5.0,),
            Text(
              '• Prevención de enfermedades laborales.\n\n• Reducción de la propagación del SARS-COV-2.\n\n• Reducción de costos.\n\n• Automatización del acceso.\n\n• Mejora en la seguridad material de la empresa.\n\n• Regulación de normas de seguridad e higiene.',
              style: kLittleGreyTextStyle.copyWith(fontSize: 20.0),
            ),
            BigDivider(),
            Text('Nuestro Sponsor', style: kLittleTitleTextStyle,),
            SizedBox(height: 20.0,),
            Row(
              children: [
                Expanded(
                  child: Column(
                    children: [
                      Text('DAKO Trailers', style: kLittleTitleTextStyle, textAlign: TextAlign.center,),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          UrlLauncherIcon(icon: FontAwesomeIcons.instagram, url: 'https://www.instagram.com/dakotrailers/',),
                          UrlLauncherIcon(icon: FontAwesomeIcons.whatsapp, url: 'https://wa.link/0588l4',),
                          UrlLauncherIcon(icon: FontAwesomeIcons.facebook, url: 'https://www.facebook.com/DAKOTrailers/',),
                        ],
                      ),
                    ],
                  ),
                ),
                Expanded(child: Image.network('https://scontent.feze12-1.fna.fbcdn.net/v/t1.18169-9/12495196_1663792903882059_1110357431269459009_n.jpg?_nc_cat=106&ccb=1-5&_nc_sid=e3f864&_nc_eui2=AeFwrk3Q5grE2oALg6EInTb6gWSJinJ7YBiBZImKcntgGDF7gRTSwAmbjOBRItlmczqHbUZ1ZVH5j37KiVmbUG2f&_nc_ohc=60rCgxIq81kAX-4551j&_nc_ht=scontent.feze12-1.fna&oh=35ca5988b0dfa843fa754f179cdee0ab&oe=61460D0D')),
              ],
            ),
            SizedBox(height: 20.0,),
            BigDivider(),
            Text('Contáctanos', style: kLittleTitleTextStyle,),
            SizedBox(height: 20.0,),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                UrlLauncherIcon(icon: FontAwesomeIcons.instagram, url: 'https://instagram.com/safe_project', size: 50.0,),
                UrlLauncherIcon(icon: FontAwesomeIcons.whatsapp, url: 'https://wa.link/nukpd7', size: 50.0,),
                UrlLauncherIcon(icon: FontAwesomeIcons.github, url: 'https://github.com/impatrq/SAFE', size: 50.0,),
              ],
            ),
            SizedBox(height: 20.0,),
          ],
        ),
      ),
    );
  }
}
class BigDivider extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(height: 20.0,),
        Divider(thickness: 3,),
        SizedBox(height: 20.0,),
      ],
    );
  }
}

