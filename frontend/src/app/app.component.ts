import {Component, OnInit} from '@angular/core';
import {Picture} from "./_models/picture.model";
import {BaseComponent} from "./base/base.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent extends BaseComponent implements OnInit {
  private base64textString = '';
  private extension = '';

  ngOnInit() {
    if (this._apiService.user.token) {
      this._apiService.verifyToken();
    }
  }

  logOut() {
    this._apiService.logout(true);
    this.showSuccess('Logged out', 'OK', 2000);
  }

  handleFileSelect(evt) {
    const files = evt.target.files;
    const file = files[0];
    if (files && file) {
      this.extension = 'data:' + file.type + ';base64,';
      const reader = new FileReader();
      reader.onload = this._handleReaderLoaded.bind(this);
      reader.readAsBinaryString(file);
    }
  }

  _handleReaderLoaded(readerEvt) {
    const binaryString = readerEvt.target.result;
    this.base64textString = this.extension + btoa(binaryString);

    this._apiService.picture = new Picture;
    this._apiService.uploading = true;

    this.showSuccess('Uploading...', null);
    this._apiService.postPicture(this.base64textString, null).subscribe(
      picture => {
        this._apiService.picture = picture;
        this.showSuccess('Upload completed. NotHotdog computing...', null, 3000);
      },
      err => {
        this._apiService.uploading = false;
        this.showError('File upload failed', 'OK');
      }
    );
  }

  endUpload() {
    this._apiService.uploading = false;
    this.router.navigate(['/result']);
  }

  handleSocketMessage(message) {
    let action = message['action'];
    let data = message['data'];

    if (action === 'compute') {
      let isHotdog: boolean = data['is_hotdog'];
      let id: string = data['id'];
      this._apiService.picture.is_hotdog = isHotdog;

      if (this._apiService.picture.id === id) {
        this.endUpload()
      }
    }
  }
}
