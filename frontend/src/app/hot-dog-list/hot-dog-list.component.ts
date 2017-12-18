import {Component, OnInit} from '@angular/core';
import {Picture} from "../_models/picture.model";
import {BaseComponent} from "../base/base.component";
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../api.service";
import {MatDialog, MatSnackBar} from "@angular/material";
import {SocketService} from "../socket.service";

@Component({
  selector: 'app-hot-dog-list',
  templateUrl: './hot-dog-list.component.html',
  styleUrls: ['./hot-dog-list.component.scss']
})
export class HotDogListComponent extends BaseComponent implements OnInit {
  public pictures: Array<Picture> = [];
  public loading = true;
  public title = 'All';
  public sub: any;

  constructor(private route: ActivatedRoute, _apiService: ApiService, public router: Router, public snackBar: MatSnackBar, public dialog: MatDialog,
              public socket: SocketService) {
    super(_apiService, router, snackBar, dialog, socket);
  }

  ngOnInit() {
    this.process();
  }

  process() {
    this.sub = this.route.params.subscribe(params => {
      let tag = params['tag'];
      this.getPhotos(tag);
      if (tag) {
        this.title = 'Tag: ' + tag;
      } else {
        this.title = 'All';
      }
    });
  }

  getPhotos(tag?: string) {
    this._apiService.getPictures(tag).subscribe(
      pictures => {
        this.pictures = pictures;
        this.loading = false;
      },
      err => {
        this.showError('Can\'t read data from server', 'OK', 3000);
        this.router.navigate(['/home']);
      }
    )
  }

  handleSocketMessage(message) {
    let action = message['action'];
    let data = message['data'];

    if (action === 'new-picture') {
      this.process();
    }

  }

}
