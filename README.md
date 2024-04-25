# RentHub

This is a multilingual (English | Arabic) django app that helps in connecting properties owners and tentas quickly.

## RentHubAPI app

(to be added)

### models.py

This file contains all the models required for the project:

| Model                                 | The Purpose                                                            |
| ------------------------------------- | ---------------------------------------------------------------------- |
| CustomUser with its CustomUserManager | To customise the user model and provide more features than the deafult |
| Owner with its OwnerManager           | To have separate user types                                            |
| Tenant with its TenantManager         | To have separate user types                                            |
| Listing                               | For owners o create property listing                                   |
| Collections                           | For tenants to save properties they like                               |
| Property Type                         | To add the property type for listings (will be used for filtering)     |
| Features                              | To add the features for listings (will be used for filtering)          |
| Image                                 | To add the images for listings                                         |

Models explained in detail in this Medium article (a link to be added)

---
