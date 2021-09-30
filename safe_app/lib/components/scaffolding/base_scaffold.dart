import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/services/auth_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/components/scaffolding/colored_safe_area.dart';
import 'package:safe_app/components/listTiles/menu_list_tile.dart';
import 'package:safe_app/components/customWidgets/nfc_available_widget.dart';
import 'package:safe_app/components/customWidgets/custom_divider.dart';
import 'package:safe_app/services/safe_app_controller.dart';

class BaseScaffold extends StatelessWidget {

  BaseScaffold({required this.userData, required this.body, this.fab});

  final userData;
  final Widget body;
  final FloatingActionButton? fab;
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey();

  final AuthController authController = AuthController();

  @override
  Widget build(BuildContext context) {
    return ColoredSafeArea(
      child: Scaffold(
        key: _scaffoldKey,
        floatingActionButton: fab,
        drawer: Drawer(
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    onPressed: () => Get.back(),
                    icon: Icon(
                      FontAwesomeIcons.times,
                      color: kLogoDarkBlueColor,
                    ),
                  ),
                  IconButton(
                    onPressed: () async {
                      await authController.logoutUser();
                      Get.offAllNamed('/login');
                    },
                    icon: Icon(
                      FontAwesomeIcons.signOutAlt,
                      color: kLogoDarkBlueColor,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 30.0,),
              CircleAvatar(
                radius: 50.0,
                backgroundColor: kLogoDarkBlueColor,
                child: Text(
                  userData['initials'],
                  style: kButtonBoldWhiteTextStyle,
                ),
              ),
              SizedBox(height: 10.0,),
              Text(
                userData['name'],
                style: kLittleTitleTextStyle,
              ),
              Text(
                userData['email'],
                style: kLittleGreyTextStyle,
              ),
              SizedBox(height: 30.0,),
              Expanded(
                child: ListView(
                  physics: BouncingScrollPhysics(),
                  // itemExtent: 30.0,
                  children: [
                    CustomDivider(),
                    MenuListTile(label: 'Dashboard', icon: Icons.tv, onTap: (){
                      Get.back();
                      // Get.offAllNamed('/dashboard');
                    }),
                    CustomDivider(),
                    MenuListTile(label: 'Empleados', icon: FontAwesomeIcons.solidAddressBook, onTap: (){
                      Get.back();
                      Get.toNamed('/workers');
                    }),
                    CustomDivider(),
                    MenuListTile(label: 'Puertas', icon: FontAwesomeIcons.doorOpen, onTap: (){
                      Get.back();
                      Get.toNamed('/doors');
                    }),
                    CustomDivider(),
                    NFCAvailableWidget(
                      blankResult: true,
                      availableWidget: Column(
                        children: [
                          MenuListTile(label: 'Buscador', icon: FontAwesomeIcons.search, onTap: (){
                            Get.back();
                            Get.toNamed('/finder');
                          }),
                          CustomDivider(),
                        ],
                      ),
                    ),
                    MenuListTile(label: 'Nosotros', icon: FontAwesomeIcons.infoCircle, onTap: (){
                      Get.back();
                      Get.toNamed('/about-us');
                    }),
                    CustomDivider(),
                  ],
                ),
              ),
              SizedBox(height: 30.0,),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset('assets/images/safe_logo.png', width: 40.0, height: 40.0,),
                  SizedBox(width: 15.0,),
                  Text('© SAFE Project 2021.', style: kLittleGreyTextStyle,),
                ],
              ),
              // MenuListTile(label: 'Configuración', icon: FontAwesomeIcons.cog, onTap: (){}),
              SizedBox(height: 30.0,),
            ],
          ),
        ),
        body: Padding(
          padding: EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GestureDetector(
                onTap: () => _scaffoldKey.currentState?.openDrawer(),
                child: Icon(
                  FontAwesomeIcons.bars,
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


