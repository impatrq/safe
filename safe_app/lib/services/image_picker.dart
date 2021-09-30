import 'package:image_picker/image_picker.dart';

class ImagePickerHelper {

  final ImagePicker _picker = ImagePicker();

  Future<dynamic> _getLostData() async {
    final LostDataResponse response = await _picker.retrieveLostData();
    if (response.isEmpty) {
      return;
    }
    if (response.file != null) {
      return response.file;
    } else {
      print('EXCEPTION ...: ${response.exception}');
    }
  }

  Future<XFile?> _getImage(ImageSource source) async {
    XFile? photo = await _picker.pickImage(source: source);
    var retrievedData = await _getLostData();
    if(retrievedData != null){
      photo = retrievedData;
    }
    return photo;
  }

  Future<XFile?> getImageFromGallery() async {
    return await _getImage(ImageSource.gallery);
  }

  Future<XFile?> getImageFromCamera() async {
    return await _getImage(ImageSource.camera);
  }

}