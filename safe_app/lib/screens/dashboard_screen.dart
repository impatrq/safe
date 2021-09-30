import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'dart:math';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/base_scaffold.dart';
import 'package:safe_app/components/customWidgets/scrollable_row.dart';
import 'package:safe_app/components/customWidgets/door_card.dart';
import 'package:safe_app/components/listTiles/dashboard_log_tile.dart';
import 'package:safe_app/services/spinning_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/services/safe_app_controller.dart';

class DashboardScreen extends StatelessWidget {

  DashboardScreen({required this.userData});

  final userData;

  final SafeAppController _safeAppController = Get.find();

  List<Widget> _getDoorsCards(doors){
    List<Widget> doorsList = [];
    doors.forEach((door) {
      doorsList.add(DoorCard(
        name: door.doorName,
        peopleInside: door.peopleInside,
        sanitizer: door.sanitizer,
        isOpened: door.isOpened,
        isSafe: door.isSafe,
        logs: door.logs,
        onTap: (){},
      ));
    });
    return doorsList;
  }

  @override
  Widget build(BuildContext context) {
    return BaseScaffold(
      userData: userData,
      body: GetBuilder<SafeAppController>(
        init: _safeAppController,
        builder: (controller) => Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Dashboard',
                  style: kMediumTitleTextStyle,
                ),
                GetBuilder<SpinningController>(
                  init: SpinningController(),
                  builder: (spinningController) => Transform.rotate(
                    angle: (spinningController.animationController!.value * 360) * pi / 180,
                    child: IconButton(
                      onPressed: () async {
                        spinningController.startSpin();
                        await controller.updateDoorsList();
                        await controller.updateLastLogsList();
                        spinningController.stopSpin();
                      },
                      icon: Icon(
                        FontAwesomeIcons.syncAlt,
                        color: kLogoDarkBlueColor,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 10.0,),
            Text('Puertas', style: kLittleTitleTextStyle.copyWith(fontSize: 18.0),),
            ScrollableRow(
              items: _getDoorsCards(controller.data.doorsList),
            ),
            SizedBox(height: 30.0,),
            Text('Historial Reciente', style: kLittleTitleTextStyle.copyWith(fontSize: 18.0),),
            Divider(thickness: 3,),
            Expanded(
              child: Scrollbar(
                radius: Radius.circular(10.0),
                child: Padding(
                  padding: EdgeInsets.only(right: 15.0),
                  child: ListView.builder(
                    physics: BouncingScrollPhysics(),
                    itemBuilder: (context, index){
                      var log = controller.data.lastLogsList[index];
                      return DashboardLogTile(
                        imageURL: log.workerProfileImage,
                        workerName: log.workerName,
                        doorName: log.doorName,
                        allowed: log.authorized,
                      );
                    },
                    itemCount: controller.data.lastLogsList.length,
                  ),
                ),
              ),
            ),
          ],
        ),
      )
    );
  }
}