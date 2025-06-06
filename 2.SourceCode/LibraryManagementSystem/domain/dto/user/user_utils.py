from domain.dto.user.user_dto import UserDTO
from domain.dto.user.user_role_dto import UserRoleDTO

def user_role_dto_to_user_dto(user_role_dto: UserRoleDTO) -> UserDTO:
    """
    Utility function to convert a UserRoleDTO object to a UserDTO object.
    """
    if user_role_dto is None:
        return None

    return UserDTO(
        user_id=user_role_dto.user_id,
        first_name=user_role_dto.first_name,
        last_name=user_role_dto.last_name,
        user_name=user_role_dto.user_name,
        password=user_role_dto.password,
        email=user_role_dto.email,
        phone=user_role_dto.phone,
        address=user_role_dto.address,
        gender=user_role_dto.gender,
        user_role_id=user_role_dto.user_role_id_fk,
        is_delete=user_role_dto.is_delete,
        is_admin=user_role_dto.is_admin,
        role_name=user_role_dto.role_name,
        created_dt=None,  # You may set default or fetch if needed
        created_by=None,
        update_dt=None,
        update_by=None
    )
