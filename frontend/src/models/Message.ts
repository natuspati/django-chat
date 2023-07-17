import {UserModel} from './User';

export interface MessageModel {
    id: string;
    room: string;
    from_user: string;
    to_user: string;
    content: string;
    timestamp: string;
    read: boolean;
}
