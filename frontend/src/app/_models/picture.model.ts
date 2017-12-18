import {Tag} from "./tag.model";
import {User} from "./user.model";

export class Picture {
  constructor(user?: User) {
    this.user = new User;
    this.owned = false;
    this.image = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    this.watermark_image = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    this.is_hotdog = false;

    if (user) {
      this.user = user;
    }
  }

  public id: string;
  public desc: string;
  public user: User;
  public image: string;
  public watermark_image: string;

  public tags: Array<Tag>;
  public is_hotdog: boolean;
  public created_at: string;

  public owned: boolean;

}
