import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/components/scaffolding/colored_safe_area.dart';

class BackArrowScaffold extends StatelessWidget {

  BackArrowScaffold({required this.body, this.fab});

  final Widget body;
  final FloatingActionButton? fab;
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    return ColoredSafeArea(
      child: Scaffold(
        key: _scaffoldKey,
        floatingActionButton: fab,
        body: Padding(
          padding: EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GestureDetector(
                onTap: () => Get.back(),
                child: Icon(
                  FontAwesomeIcons.arrowLeft,
                  color: kLogoDarkBlueColor,
                ),
              ),
              SizedBox(height: 10.0,),
              Expanded(child: body),
            ],
          ),
        ),
      ),
    );
  }
}