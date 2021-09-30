import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'dart:math';
import 'dart:convert';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/back_arrow_scaffold.dart';
import 'package:safe_app/components/listTiles/doors_list_tile.dart';
import 'package:safe_app/services/spinning_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/services/qr_reader.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/forms/door_add_form.dart';

class DoorsScreen extends StatelessWidget {

  final SafeAppController _safeAppController = Get.find();

  final TextEditingController _doorSearchBarController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return BackArrowScaffold(
        body: GetBuilder<SafeAppController>(
          init: _safeAppController,
          builder: (controller) => Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Puertas',
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
                          _doorSearchBarController.clear();
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
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _doorSearchBarController,
                      onChanged: (newValue){},
                      decoration: InputDecoration(
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(5.0),
                          borderSide: BorderSide(
                              width: 1.0,
                              color: Colors.grey
                          ),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(5.0),
                          borderSide: BorderSide(
                              width: 2.0,
                              color: Colors.grey
                          ),
                        ),
                        hintText: 'Buscar por nombre / sector',
                        contentPadding: EdgeInsets.all(12.0),
                        isCollapsed: true,
                      ),
                    ),
                  ),
                  SizedBox(width: 15.0,),
                  IconButton(
                    onPressed: () async {
                      // loadingController.toggleLoadingState();

                      if(_doorSearchBarController.text == ''){
                        controller.updateDoorsList();
                      } else {
                        controller.searchDoor(_doorSearchBarController.text);
                      }

                      // loadingController.toggleLoadingState();
                    },
                    icon: Icon(FontAwesomeIcons.search, color: kLogoDarkBlueColor,),
                  ),
                ],
              ),
              SizedBox(height: 10.0,),
              Text(
                '*Se aconseja rellenar los depósitos cuando el nivel del sanitizante sea menor al 20%',
                style: kLittleGreyTextStyle.copyWith(fontSize: 12.0),
              ),
              Align(
                alignment: Alignment.centerRight,
                child: IconButton(
                  onPressed: (){
                    Get.bottomSheet(
                      CustomQRView(
                        onRead: (String data){
                          var res = jsonDecode(data);
                          Get.bottomSheet(
                              DoorBottomSheetAddForm(mac: res['mac'], sanitizer: res['sanitizer'])
                          );
                        },
                      ),
                    );
                  },
                  icon: Icon(
                    FontAwesomeIcons.plus,
                    color: kLogoDarkBlueColor,
                  ),
                ),
              ),
              Divider(thickness: 2,),
              Row(
                // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Expanded(
                    flex: 2,
                    child: Text(
                      'Sector - Puerta',
                      style: kTableHeaderTextStyle,
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Expanded(
                    child: Text(
                      'Sanitizante',
                      style: kTableHeaderTextStyle,
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Expanded(
                    child: Text(
                      'Seguro',
                      style: kTableHeaderTextStyle,
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
              Divider(thickness: 2,),
              Expanded(
                child: Scrollbar(
                  radius: Radius.circular(10.0),
                  child: Padding(
                    padding: EdgeInsets.only(right: 5.0),
                    child: ListView.builder(
                      physics: BouncingScrollPhysics(),
                      itemBuilder: (context, index){
                        var door = controller.data.doorsList[index];
                        return DoorListTile(
                          name: door.doorName,
                          peopleInside: door.peopleInside,
                          sanitizer: door.sanitizer,
                          isOpened: door.isOpened,
                          isSafe: door.isSafe,
                          logs: door.logs,
                        );
                      },
                      itemCount: controller.data.doorsList.length,
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