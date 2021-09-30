import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:safe_app/utilities/constants.dart';

class UrlLauncherIcon extends StatelessWidget {

  UrlLauncherIcon({required this.icon, required this.url, this.size});

  final IconData icon;
  final String url;
  final double? size;

  void _launchURL() async =>
      await canLaunch(url) ? await launch(url) : throw 'Could not launch $url';

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _launchURL,
      child: Icon(
        icon,
        color: kLogoDarkBlueColor,
        size: size,
      ),
    );
  }
}
